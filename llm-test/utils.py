import os
import yaml
import pickle
from tqdm import tqdm
import json
from typing import Any, Dict, List
from unstructured.partition.auto import partition
from unstructured.cleaners.core import clean

from langchain.vectorstores import Chroma
from langchain.retrievers import BM25Retriever
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


def load_config(path="config.yaml"):
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    return config

def get_elements(data_folder: str = "./data") -> dict:
    elements_dict = {}
    for file in tqdm(os.listdir(data_folder), desc="Processing files"):
        file_path = os.path.join(data_folder, file)
        if os.path.isfile(file_path):
            elements_dict[file] = partition(
                                    filename=file_path,
                                    include_page_breaks=False,
                                    strategy="hi_res",
                                    languages=["eng", "rus"],
                                    extract_images_in_pdf=False,
                                )
    return elements_dict

def get_documents(
    elements_dict: Dict[str, List[Any]],
) -> List[Document]:
    documents = []
    file_key = "file_path"
    file = "filename"
    page = "page_number"
    title = "title"
    
    for _, page_elements in elements_dict.items():
        for element in page_elements:
            metadata = {
                file: str(element.metadata.filename),
                file_key: str("/".join([element.metadata.file_directory, element.metadata.filename])),
                page: str(element.metadata.page_number),
                title: "".join(element.text.split("\n", 1)[0]).strip(),
            }
            documents.append(Document(
                page_content=clean(
                    element.text,
                    extra_whitespace=True,
                    dashes=True,
                    bullets=True,
                    trailing_punctuation=True,
                    lowercase=False,
                ),
                metadata=metadata,
            ))


    return documents

def get_db(embeddings,documents,index_folder: str = "./data/index/"):
    chroma_db = Chroma.from_documents(
        documents=documents,
        persist_directory=index_folder,
        embedding=embeddings,
    ).as_retriever()

    bm_25 = BM25Retriever.from_documents(documents=documents, k=3)

    with open(os.path.join(index_folder, "bm25.pickle"), "wb") as handle:
        pickle.dump(bm_25, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return chroma_db, bm_25

def rerank_docs(history, retrieved_docs, top_n: int = 3) -> List:
    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    reranked_docs = []
    for doc in retrieved_docs:
        sentence_pair = [history, doc.page_content]
        score = cross_encoder.predict([sentence_pair])[0]
        doc.metadata["mean_rerank_score"] = score
        reranked_docs.append(doc)
    reranked_docs = sorted(
        reranked_docs, key=lambda x: x.metadata["mean_rerank_score"], reverse=True
    )
    top_n_docs = reranked_docs[:top_n]
    return top_n_docs

def get_history_json(
    json_path: str = "./history.json",
    history=None,
) -> List:
    if not history:
        with open(json_path, "r", encoding="UTF-8") as f:
            history = json.load(f)

    history["context"].append({"role": "assistant", "content": None})
    raw_list: List[str] = [i["content"] for i in history["context"]]
    history_list: List[List[str]] = []
    for i in range(0, len(raw_list), 2):
        history_list.append(raw_list[i : i + 2])

    if len(history_list[-1]) == 1:
        history_list[-1].append(None)
    return history_list



def get_relevant_documents(
    ensemble_retriever,
    history
):
    retrieved_docs = ensemble_retriever.get_relevant_documents(history[-1][0])

    if len(retrieved_docs) == 0:
        retrieved_docs = "Ничего не найдено!"

    return retrieved_docs
