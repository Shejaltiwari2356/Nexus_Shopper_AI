import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(persist_directory="./memory/chroma")
)

collection = client.get_or_create_collection(
    name="user_preferences"
)

def store_preference(user_id: str, text: str):
    collection.add(
        documents=[text],
        metadatas=[{"user_id": user_id}],
        ids=[f"{user_id}_{len(collection.get()['ids'])}"]
    )

def retrieve_preferences(user_id: str, limit: int = 3):
    results = collection.query(
        query_texts=["user preferences"],
        n_results=limit,
        where={"user_id": user_id}
    )
    return results.get("documents", [[]])[0]
