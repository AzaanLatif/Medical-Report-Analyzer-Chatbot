# backend/retriever.py

import os
import pickle
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.schema import BaseRetriever, Document
from typing import List, Any
from pydantic import Field
import faiss
import numpy as np

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

FAISS_INDEX_PATH = "faiss_index"

def load_faiss():
    """Load FAISS index and chunks."""
    index = faiss.read_index(f"{FAISS_INDEX_PATH}/index.faiss")
    with open(f"{FAISS_INDEX_PATH}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def retrieve_relevant_chunks(query, top_k=3):
    """Find top_k relevant chunks for a query."""
    index, chunks = load_faiss()
    query_vector = embeddings.embed_query(query)
    
    # Search FAISS
    distances, indices = index.search([query_vector], top_k)

    results = []
    for i in range(len(indices[0])):
        if indices[0][i] != -1:
            results.append(chunks[indices[0][i]])
    return results

class SimpleRetriever(BaseRetriever):
    index: faiss.Index = Field(description="FAISS index for similarity search")
    chunks: List[str] = Field(description="List of text chunks")
    embeddings: Any = Field(description="Embeddings model")
    top_k: int = Field(default=3, description="Number of documents to retrieve")

    class Config:
        arbitrary_types_allowed = True

    def get_relevant_documents(self, query: str) -> List[Document]:
        query_vector = self.embeddings.embed_query(query)
        # Convert query vector to numpy array
        query_vector = np.array([query_vector], dtype=np.float32)  # Add this line
        distances, indices = self.index.search(query_vector, self.top_k)
        results = []
        for i in range(len(indices[0])):
            if indices[0][i] != -1:
                doc = Document(
                    page_content=self.chunks[indices[0][i]],
                    metadata={"score": float(distances[0][i])}
                )
                results.append(doc)
        return results

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)

def create_retriever():
    index, chunks = load_faiss()
    return SimpleRetriever(
        index=index,
        chunks=chunks,
        embeddings=embeddings,
        top_k=3
    )

