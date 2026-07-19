import streamlit as st
import os
import sys
import time

def stream_text(text):
    """Simulates a live typing effect."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04)

# Ensure Python can find both the root folder and the core folder
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
core_path = os.path.join(root_path, 'core')
sys.path.append(root_path)
sys.path.append(core_path)

from core.document_extractor import extract_text
from core.text_chunker import chunk_text
from core.embedding_generator import generate_embeddings
from core.vector_store import create_and_save_index
from core.semantic_search import load_database, search_documents
from core.answer_generator import generate_answer
from core.summarizer import generate_summary

# --- Page Configuration ---
st.set_page_config(page_title="Smart Document Q&A", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Welcome screen hero styling */
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #4A90E2, #9013FE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #6c757d;
        margin-top: 10px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize Session States ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest" # Default name if none is provided
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db_ready" not in st.session_state:
    st.session_state.db_ready = False
if "document_summary" not in st.session_state:
    st.session_state.document_summary = ""
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

# ==========================================
# VIEW 1: THE WELCOME SCREEN
# ==========================================
if not st.session_state.app_started:
    st.write("<br><br>", unsafe_allow_html=True)
    
    st.markdown('<div class="hero-title">Smart Document AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Turn static files into an interactive, intelligent knowledge base.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### ⚡ Instant Summaries\nUpload massive documents and instantly receive crisp, executive-level summaries.")
    with col2:
        st.warning("### 🔍 Semantic Search\nDon't rely on keywords. Search your documents using true contextual understanding.")
    with col3:
        st.success("### 💬 Generative Q&A\nAsk natural questions and get precise answers backed by exact source citations.")
    
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Center the name input and launch button
    _, btn_col, _ = st.columns([1, 1.5, 1])
    with btn_col:
        # Request the user's name
        entered_name = st.text_input("Enter your name to personalize your workspace:", placeholder="e.g., Parth")
        
        if st.button("Launch Workspace 🚀", type="primary", use_container_width=True):
            # Save the name (or keep "Guest" if they leave it blank)
            if entered_name.strip():
                st.session_state.user_name = entered_name.strip()
                
            st.session_state.app_started = True
            st.rerun() 

# ==========================================
# VIEW 2: THE MAIN APPLICATION
# ==========================================
else:
    # --- Sidebar Component ---
    with st.sidebar:
        st.title(f"🏢 {st.session_state.user_name}'s Files")
        st.markdown("Upload your knowledge base to start interacting with your documents.")
        st.divider()
        
        st.header("1. Upload Documents")
        uploaded_files = st.file_uploader(
            "Supported formats: PDF, DOCX, PPTX", 
            type=['pdf', 'docx', 'pptx'], 
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.info(f"📂 {len(uploaded_files)} file(s) staged.")
            
            if st.button("⚙️ Process & Index", type="primary", use_container_width=True):
                with st.spinner("Analyzing and indexing documents..."):
                    all_raw_text = ""
                    
                    import os
                    # Ensure the data directory exists
                    if not os.path.exists("data"):
                        os.makedirs("data")
                    for uploaded_file in uploaded_files:
                        save_path = os.path.join("data", uploaded_file.name)
                        with open(save_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        all_raw_text += extract_text(save_path) + "\n\n"
                    
                    if all_raw_text.strip():
                        st.session_state.document_summary = generate_summary(all_raw_text)
                        chunks = chunk_text(all_raw_text)
                        st.session_state.chunk_count = len(chunks)
                        embeddings = generate_embeddings(chunks)
                        create_and_save_index(embeddings, chunks)
                        
                        st.session_state.db_ready = True
                        st.toast("Knowledge base built successfully!", icon="✅")
                    else:
                        st.error("⚠️ Could not extract text from the uploaded files.")
        
        if st.session_state.db_ready:
            st.divider()
            st.markdown("### 📊 Database Metrics")
            st.metric(label="Text Chunks Indexed", value=st.session_state.chunk_count)
            st.caption("FAISS Vector Database Active")
        
        st.divider()
        if st.button("⬅️ Back to Home"):
            st.session_state.app_started = False
            st.rerun()

    # --- Main Interface ---
    if not st.session_state.db_ready:
        # Personalized welcome message before documents are uploaded
        st.title(f"👋 Welcome, {st.session_state.user_name}!")
        st.info("👈 Please upload and process a document in the sidebar to begin.")
        
    else:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title(f"🧠 {st.session_state.user_name}'s Active Workspace")
        with col2:
            # Inject empty space to push the button down to align with the title
            st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
            st.button("Clear Chat", on_click=lambda: st.session_state.chat_history.clear(), use_container_width=True)
            
        tab_chat, tab_summary = st.tabs(["💬 Chat Q&A", "📌 Executive Summary"])

        with tab_summary:
            st.markdown("### Document Overview")
            st.markdown(st.session_state.document_summary)
            
            st.divider()
            st.download_button(
                label="📥 Download Summary as Text",
                data=st.session_state.document_summary,
                file_name=f"{st.session_state.user_name}_document_summary.txt",
                mime="text/plain",
                type="primary"
            )

        with tab_chat:
            for message in st.session_state.chat_history:
                avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
                    
                    if "sources" in message and message["sources"]:
                        with st.expander("🔍 View Source Documents"):
                            for i, source_text in enumerate(message["sources"]):
                                st.markdown(f"**Source {i+1}:**\n {source_text}")
                                st.divider()

            if user_question := st.chat_input("Ask something about your documents..."):
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(user_question)
                
                st.session_state.chat_history.append({"role": "user", "content": user_question})
                
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Searching knowledge base..."):
                        db_index, db_chunks = load_database()
                        context_chunks = search_documents(user_question, db_index, db_chunks)
                        ai_response = generate_answer(user_question, context_chunks)
                        
                        st.write_stream(stream_text(ai_response))
                        
                        with st.expander("🔍 View Source Documents"):
                            for i, source_text in enumerate(context_chunks):
                                st.markdown(f"**Source {i+1}:**\n {source_text}")
                                st.divider()
                
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "sources": context_chunks
                })