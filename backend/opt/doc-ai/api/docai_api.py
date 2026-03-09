from fastapi import FastAPI
import chromadb
from sentence_transformers import SentenceTransformer

app = FastAPI()

# abrir banco vetorial existente
client = chromadb.PersistentClient(
    path="/opt/doc-ai/vector_db"
)

# ajustar depois conforme nome da collection
collection = client.get_collection("biblioteca")

# modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/search")
def search(q: str):

    embedding = model.encode(q).tolist()

    res = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    results = []

    for i in range(len(res["documents"][0])):

        meta = res["metadatas"][0][i]

        results.append({

            "arquivo": meta.get("arquivo"),
            "pagina": meta.get("pagina"),
            "trecho": res["documents"][0][i],
            "score": res["distances"][0][i]

        })

    return {
        "query": q,
        "results": results
    }