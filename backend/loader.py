# backend/loader.py

import os
import faiss
import pickle
import numpy as np
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Directory to save FAISS index
FAISS_INDEX_PATH = "faiss_index"

def load_pdf(file_path):
    """Read and extract text from a PDF file."""
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def split_text(text, chunk_size=1000, chunk_overlap=100):
    """Split text into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def create_and_store_faiss(chunks):
    # Create embeddings
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert text chunks to vectors
    vectors = [embeddings.embed_query(chunk) for chunk in chunks]
    vectors = np.array(vectors, dtype=np.float32)
    
    # Create FAISS index
    dimension = len(vectors[0])
    vectorstore = faiss.IndexFlatL2(dimension)
    
    # Add vectors to the index
    vectorstore.add(vectors)
    
    # Save index and chunks
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    faiss.write_index(vectorstore, f"{FAISS_INDEX_PATH}/index.faiss")
    with open(f"{FAISS_INDEX_PATH}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    print("[SUCCESS] FAISS index created and saved.")  # Changed from emoji to plain text

def process_pdf(file_path):
    """Complete pipeline: load PDF → split → embed → store."""
    text = load_pdf(file_path)
    chunks = split_text(text)
    create_and_store_faiss(chunks)
    return True  # Indicates successful processing
