import os
import json
from langchain.embeddings import HuggingFaceEmbeddings
from huggingface_hub import hf_hub_download, snapshot_download
from llama_cpp import Llama

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def set_roles(config):
    role_tokens = {
        "user": config["user_token"],
        "assistant": config["assistant_token"],
        "system": config["system_token"],
    }

    return role_tokens


def load_model(model_path, repo_name, model_name, model_params):
    if not os.path.isfile(model_path):
        model_path = hf_hub_download(
            repo_id=repo_name,
            filename=model_name,
            local_dir="./models/llm/",
            local_dir_use_symlinks=False,
            force_download=False,
            resume_download=True,
        )
    else:
        model_path = model_path

    model = Llama(
        model_path=model_path,
        n_ctx=model_params["max_context"],
        n_gpu_layers=-1,
        n_parts=model_params["n_parts"],
        logits_all=True
    )

    return model


def load_embeddings(embeddings_repo, embeddings_path):
    if not os.path.isdir(embeddings_path):
        embedding_path = snapshot_download(
            repo_id=embeddings_repo, cache_dir=embeddings_path
        )
    else:
        embedding_path = embeddings_path

    embeddings = HuggingFaceEmbeddings(
        model_name=embeddings_repo, cache_folder=embedding_path
    )
    return embeddings


def tokenize_message(model, role, content, config):
    role_tokens = set_roles(config)
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, role_tokens[role])
    message_tokens.insert(2, config["linebreak_token"])
    message_tokens.append(model.token_eos())

    return message_tokens

def create_response(response, retrieved_docs):
    response_text = response[-1][-1]
    if response_text == "" or response_text is None:
        response_data = {"response": response_text, "token_count": 0}
    else:
        response_data = {
            "response": response_text,
            **{
                f"paragraph{i}": {
                    "content": doc.page_content,
                    "src": {
                        "file_path": doc.metadata["file_path"],
                        "file_name": doc.metadata["filename"],
                        "page_number": doc.metadata["page_number"],
                    },
                }
                for i, doc in enumerate(retrieved_docs)
            },
        }

    with open("response.json", "w") as f:
        json.dump(response_data, f, ensure_ascii=False, indent=4)

    return response_data

def get_response(
    history,
    model,
    retrieved_docs,
    config,
):
    if not history:
        return

    system_message = {"role": "system", "content": config["system_prompt"]}
    tokens = tokenize_message(model, config=config, **system_message)
    tokens.append(config["linebreak_token"])
    for user_message, assistant_message in history[:-1]:
        message_tokens = tokenize_message(
            model=model, role="user", content=user_message, config=config
        )
        tokens.extend(message_tokens)
        if assistant_message:
            message_tokens = tokenize_message(
                model=model, role="assistant", content=assistant_message, config=config
            )
            tokens.extend(message_tokens)

    last_user_message = history[-1][0]
    if retrieved_docs:
        context = ". ".join(doc.page_content for doc in retrieved_docs).split()[:config["model_params"]["max_context"]]
        last_user_message = f"Контекст: {context}\n\n Используя контекст, ответьте на вопрос: {last_user_message}. При ответе на вопрос используйте ТОЛЬКО сведения из контекста. Пожалуйста, соблюдайте стилистику, грамматику и морфологию русского языка для корректного написания ответа."
    message_tokens = tokenize_message(
        model=model, role="user", content=last_user_message, config=config
    )
    tokens.extend(message_tokens)

    role_tokens = [
        model.token_bos(),
        config["assistant_token"],
        config["linebreak_token"],
    ]
    tokens.extend(role_tokens)

    generator = model.generate(
        tokens, top_k=config["top_k"], top_p=config["top_p"], temp=config["temp"]
    )

    partial_text = ""
    for i, token in enumerate(generator):
        if token == model.token_eos() or (
            config["max_new_tokens"] is not None and i >= config["max_new_tokens"]
        ):
            break
        partial_text += model.detokenize([token]).decode("utf-8", "ignore")
        history[-1][1] = partial_text

    return create_response(history, retrieved_docs)
