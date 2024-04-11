from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from utils import (
    get_relevant_documents,
    rerank_docs,
    get_history_json,
)
from init_model import get_response
from main import (
    ensemble_retriever,
    model,
    config,
)
import threading

app = FastAPI()
mutex = threading.Lock()

@app.post("/api/response/")
def response(request: dict[str, list[dict[str, str]]], echo: bool = False):
    if echo:
        response = {
            "Response": request["context"][-1]["content"]
        }
        return JSONResponse(content=response, status_code=200)
    else:
        history = get_history_json(history=request)
        
        retrieved_docs = get_relevant_documents(
            ensemble_retriever, history
        )
        
        if retrieved_docs != "Ничего не найдено!":
            retrieved_docs = rerank_docs(history[-1][0], retrieved_docs)
        
        mutex.acquire()
        response = get_response(history, model, retrieved_docs, config)
        mutex.release()
        
        return JSONResponse(content=response, status_code=200)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=7777)
