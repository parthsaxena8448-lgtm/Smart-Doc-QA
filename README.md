# 🧠 Smart Document AI

**Smart Document AI** is an enterprise-grade, RAG-powered (Retrieval-Augmented Generation) document intelligence platform. It transforms static, unstructured files (PDF, DOCX, PPTX) into an interactive, conversational knowledge base, allowing users to extract summaries and ask context-aware questions with source transparency.

## 🚀 Key Features

*   **Executive Summarization:** Generates instant, structured executive summaries for any uploaded document.
*   **Semantic RAG Pipeline:** Utilizes FAISS vector storage and Google Gemini AI to perform deep, context-aware semantic searches rather than simple keyword matching.
*   **Source Transparency:** Every AI-generated answer includes expandable source citations, ensuring the model provides verifiable, grounded information.
*   **Interactive Dashboard:** A premium, personalized UI built with Streamlit, featuring a dedicated welcome screen, session management, and metrics dashboard.
*   **Performance Metrics:** Real-time visibility into database indexing and processing throughput.

## 🛠️ Technology Stack

*   **Framework:** Streamlit (UI/Frontend)
*   **LLM & Embeddings:** Google Gemini AI (via LangChain)
*   **Vector Database:** FAISS (Facebook AI Similarity Search)
*   **Language:** Python 3.9+

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/smart-doc-qa.git](https://github.com/your-username/smart-doc-qa.git)
   cd smart-doc-qa

2. Set up virtual environment:

Bash
python -m venv venv
source venv/bin/activate

3. Install dependencies:

Bash
pip install -r requirements.txt

4. Configure environment variables:
Create a .env file in the root directory and add your Google Gemini API key:

Plaintext
GOOGLE_API_KEY=your_actual_api_key_here

## Roadmap & Architecture


This project was developed with a modular architecture, separating the core backend (extraction, chunking, embedding) from the frontend (Streamlit). It follows a standard RAG pattern:

Extraction: Parsing raw document text.

Chunking: Segmenting text into semantically meaningful blocks.

Embedding: Converting text into high-dimensional vectors.

Retrieval: Using vector similarity to surface relevant context.

Generation: Synthesizing the final answer using Gemini AI.

Built by Parth Saxena Btech CSE (AI/ML)