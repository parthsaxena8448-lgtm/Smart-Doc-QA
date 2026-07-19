import faiss
import numpy as np
import pickle
import os

def create_and_save_index(embeddings, chunks, index_path="data/faiss_index.bin", chunks_path="data/chunks.pkl"):
    """
    Creates a FAISS vector database and saves it alongside the text chunks.
    """
    # 1. FAISS requires our numbers to be in a specific format (float32 numpy array)
    embeddings_array = np.array(embeddings).astype('float32')
    
    # 2. Get the dimension (size) of our vectors (all-MiniLM-L6-v2 outputs 384 numbers per chunk)
    dimension = embeddings_array.shape[1]
    
    # 3. Create a basic FAISS index that measures distance (L2 = Euclidean distance)
    index = faiss.IndexFlatL2(dimension)
    
    # 4. Add our translated number vectors into the database
    index.add(embeddings_array)
    
    # 5. Save the database to our data folder
    faiss.write_index(index, index_path)
    
    # 6. Save the actual text chunks so we can retrieve the words later
    with open(chunks_path, "wb") as f:
        pickle.dump(chunks, f)
        
    return index

# --- Testing Section ---
if __name__ == "__main__":
    from document_extractor import extract_text
    from text_chunker import chunk_text
    from embedding_generator import generate_embeddings
    
    test_file_path = "data/test.pdf" 
    
    print("1. Processing document...")
    raw_text = extract_text(test_file_path)
    document_chunks = chunk_text(raw_text)
    
    print("2. Generating embeddings...")
    chunk_embeddings = generate_embeddings(document_chunks)
    
    print("3. Storing in FAISS database...")
    # This will create 'faiss_index.bin' and 'chunks.pkl' in your data folder
    create_and_save_index(chunk_embeddings, document_chunks)
    
    print("\nDatabase saved successfully! Check your 'data' folder for the new files.")