import faiss
import pickle
import numpy as np
from embedding_generator import get_embedding_model

def load_database(index_path="data/faiss_index.bin", chunks_path="data/chunks.pkl"):
    """
    Loads the saved FAISS database and the text chunks back into memory.
    """
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def search_documents(query, index, chunks, top_k=2):
    """
    Translates a question into numbers and finds the closest matching text chunks.
    """
    model = get_embedding_model()
    
    # 1. Translate the text question into a numerical vector
    query_vector = model.encode([query])
    query_array = np.array(query_vector).astype('float32')
    
    # 2. Search FAISS for the 'top_k' closest matches
    distances, indices = index.search(query_array, top_k)
    
    # 3. Retrieve the actual English text for those matches
    results = []
    # indices[0] contains the ID numbers of the matching chunks
    for i in indices[0]:
        if i != -1:  # -1 means FAISS couldn't find enough matches
            results.append(chunks[i])
            
    return results

# --- Testing Section ---
if __name__ == "__main__":
    print("1. Loading database...")
    db_index, db_chunks = load_database()
    
    # Looking at your previous screenshot, your document was about a Web Developer Internship
    # Let's ask a question relevant to that document
    question = "What is the duration of the internship?"
    print(f"\nQuestion: {question}")
    print("\n2. Searching for the answer in your documents...\n")
    
    relevant_chunks = search_documents(question, db_index, db_chunks)
    
    for i, chunk in enumerate(relevant_chunks):
        print(f"--- Top Match #{i+1} ---")
        print(chunk)
        print("-" * 30 + "\n")