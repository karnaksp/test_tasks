from utils import load_config, get_db, get_elements, get_documents
from init_model import load_embeddings, load_model
from langchain.retrievers import EnsembleRetriever

config = load_config()

model = load_model(
    model_path=config["model_path"],
    repo_name=config["repo_name"],
    model_name=config["model_name"],
    model_params=config["model_params"],
)

elements_dict = get_elements(config["data_path"])

documents = get_documents(elements_dict)

embeddings = load_embeddings(
    embeddings_path=config["embeddings_path"], embeddings_repo=config["embeddings_repo"]
)

chroma_db, bm25_db = get_db(
    embeddings=embeddings,
    documents=documents,
    index_folder=config["index_path"],
)

ensemble_retriever = EnsembleRetriever(
        retrievers=[chroma_db, bm25_db], weights=[0.5, 0.5]
    )
