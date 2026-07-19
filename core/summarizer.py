import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def generate_summary(raw_text):
    """
    Takes the full text of a document and generates a structured summary using Gemini.
    """
    # Initialize the latest Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)
    
    # If the document is absolutely massive, we slice it down to protect the context window
    # gemini-3.5-flash handles massive contexts, but for a quick summary, 
    # the first 40,000 characters are usually more than enough.
    text_to_summarize = raw_text[:40000]
    
    prompt = f"""
    You are an expert document analyzer. Provide a professional, concise summary of the following text.
    Use the following exact structure for your response:
    
    ### 📌 Executive Summary
    (A brief 2-3 sentence overview of the document)
    
    ### 🔑 Key Takeaways
    * (Bullet point 1)
    * (Bullet point 2)
    * (Bullet point 3)
    
    Text:
    {text_to_summarize}
    """
    
    response = llm.invoke(prompt)
    return response.content

# --- Testing Section ---
if __name__ == "__main__":
    from document_extractor import extract_text
    
    test_file_path = "data/test.pdf"
    print("1. Extracting text for summary...")
    text = extract_text(test_file_path)
    
    print("2. Generating summary via Gemini...")
    summary_result = generate_summary(text)
    
    print("\n--- DOCUMENT SUMMARY ---")
    print(summary_result)
    print("------------------------")