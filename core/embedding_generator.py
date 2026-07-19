from sentence_transformers import SentenceTransformer

def get_embedding_model():
    """
    Downloads (if necessary) and loads the Sentence Transformer model.
    """
    # This is the exact, lightweight model specified in your roadmap
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def generate_embeddings(chunks):
    """
    Takes our text chunks and translates them into numerical vectors.
    """
    model = get_embedding_model()
    
    # The .encode() function does the actual translation to numbers
    embeddings = model.encode(chunks)
    
    return embeddings

# --- Testing Section ---
if __name__ == "__main__":
    from document_extractor import extract_text
    from text_chunker import chunk_text
    
    test_file_path = "data/test.pdf" 
    
    print("1. Extracting and chunking text...")
    raw_text = extract_text(test_file_path)
    document_chunks = chunk_text(raw_text)
    
    print(f"2. Generating embeddings for {len(document_chunks)} chunks...")
    print("(Note: This might take a few seconds the very first time as it downloads the model)")
    
    chunk_embeddings = generate_embeddings(document_chunks)
    
    print(f"\nSuccess! Created {len(chunk_embeddings)} embeddings.")
    print("Here is what the first 5 numbers of Chunk #1's embedding look like:")
    print(chunk_embeddings[0][:5])