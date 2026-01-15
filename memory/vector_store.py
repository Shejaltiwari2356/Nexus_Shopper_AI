import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./memory/chroma"))
collection = client.get_or_create_collection(name="user_preferences")

def store_preference(user_id: str, text: str):
    count = len(collection.get()['ids'])
    collection.add(
        documents=[text],
        metadatas=[{"user_id": user_id}],
        ids=[f"{user_id}_{count}"]
    )

def retrieve_preferences(user_id: str, current_query: str, limit: int = 3):
    """Retrieves past preferences RELEVANT to the current search."""
    results = collection.query(
        query_texts=[current_query], # Improved: Contextual search
        n_results=limit,
        where={"user_id": user_id}
    )
    # Flatten the results
    docs = results.get("documents", [[]])[0]
    return ". ".join(docs) if docs else "No relevant past preferences found."