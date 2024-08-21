from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()
QDRANT_URL = "http://localhost:6333"

class Document(BaseModel):
    id: str
    vector: list
    text: str

class QueryRequest(BaseModel):
    query_vector: list
    top_k: int = 5

@app.post("/ingest")
def ingest_document(doc: Document):
    response = requests.put(f"{QDRANT_URL}/collections/my_collection/points/{doc.id}", json={
        "vector": doc.vector,
        "payload": {"text": doc.text}
    })
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to ingest document.")
    return {"status": "success"}

@app.post("/query")
def query_documents(query: QueryRequest):
    response = requests.post(f"{QDRANT_URL}/collections/my_collection/points/search", json={
        "vector": query.query_vector,
        "top": query.top_k
    })
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to query documents.")
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
