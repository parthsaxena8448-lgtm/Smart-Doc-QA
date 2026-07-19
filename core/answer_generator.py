import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# This line automatically searches for your .env file and loads the key into memory
load_dotenv()

def generate_answer(question, context_chunks):
    """
    Takes the user's question and the retrieved text chunks,
    and asks Gemini to answer the question using ONLY that text.
    """
    # 1. Initialize the Gemini model 
    # (temperature=0.3 makes the AI more focused and factual rather than creative)
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)
    
    # 2. Combine the retrieved paragraphs into one single block of text
    context_text = "\n\n---\n\n".join(context_chunks)
    
    # 3. Create a strict prompt for the AI
    prompt = f"""
    You are a highly accurate assistant. Use the following pieces of retrieved context to answer the user's question. 
    If the answer is not contained in the context, do not guess. Simply say "I don't know based on the provided documents."
    
    Context:
    {context_text}
    
    Question: {question}
    
    Answer:
    """
    
    # 4. Send the prompt to Gemini and get the response
    response = llm.invoke(prompt)
    
    return response.content

# --- Testing Section ---
if __name__ == "__main__":
    from semantic_search import load_database, search_documents
    
    print("1. Loading database...")
    db_index, db_chunks = load_database()
    
    # Let's ask a question we know is in your internship document
    test_question = "What happens if I successfully complete the program?"
    print(f"Question: {test_question}\n")
    
    print("2. Retrieving relevant context...")
    relevant_chunks = search_documents(test_question, db_index, db_chunks)
    
    print("3. Asking Gemini to generate a response...\n")
    final_answer = generate_answer(test_question, relevant_chunks)
    
    print("--- AI RESPONSE ---")
    print(final_answer)
    print("-------------------")