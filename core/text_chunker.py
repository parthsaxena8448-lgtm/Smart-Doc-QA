from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Breaks a large string of text into smaller, overlapping chunks.
    """
    # LangChain's smart splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    # Do the actual splitting
    chunks = text_splitter.split_text(text)
    
    return chunks

# --- Testing Section ---
if __name__ == "__main__":
    # Import your extractor from the other file!
    from document_extractor import extract_text
    
    test_file_path = "data/test.pdf" 
    
    print("1. Extracting text...")
    raw_text = extract_text(test_file_path)
    
    print("2. Chunking text...")
    document_chunks = chunk_text(raw_text)
    
    print(f"\nTotal chunks created: {len(document_chunks)}")
    
    if len(document_chunks) > 0:
        print("\n--- Here is Chunk #1 ---")
        print(document_chunks[0])
        
        if len(document_chunks) > 1:
            print("\n--- Here is Chunk #2 (Notice the overlap!) ---")
            print(document_chunks[1])