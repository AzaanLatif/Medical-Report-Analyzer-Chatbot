🩺 Medical Report Analyzer Chatbot












📝 Description

The Medical Report Analyzer Chatbot is an AI-powered tool that helps patients understand their medical reports in clear, patient-friendly language.
It extracts key findings, explains medical terms in simple words, and suggests which specialist to consult.

Developed in just 4 hours during an in-house hackathon, this project showcases how AI + NLP can bridge the gap between healthcare professionals and patients.

✨ Features

📄 Upload Medical Reports in PDF or text format

🔍 Extract Key Findings from the report

🗣 Explain Medical Terms in everyday language

💡 Recommend Specialists based on report analysis

💬 Gradio-based interactive chatbot interface

⚡ Fast and lightweight prototype

🔧 Technology Stack

Backend: Python, Flask

Frontend: Gradio

AI/ML: OpenAI GPT, LangChain

Vector Search: FAISS

PDF Processing: PyPDF2

🛠️ Prerequisites

Python 3.8+

OpenAI API key

🚀 Setup Instructions

Clone the repository

git clone https://github.com/your-username/medical-report-analyzer.git
cd medical-report-analyzer


Create a virtual environment & activate it

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Set up environment variables
Create a .env file in the root directory:

OPENAI_API_KEY=your_api_key_here


Run the application

python backend/app.py


Access the Gradio interface
The terminal will show a local URL (e.g., http://127.0.0.1:7860) — open it in your browser.

📁 File Structure
medical-report-analyzer/
│
├── .git/                  # Git version control  
├── backend/               # Backend code (Flask API, chatbot logic, PDF parsing)  
├── faiss_index/           # FAISS vector index files for semantic search  
├── venv/                  # Python virtual environment  
├── .env                   # Environment variables (API keys, configs)  
├── .gitignore             # Ignored files & folders  
├── requirements           # Python dependencies  


ℹ️ Additional Information

Gradio is used for the chatbot’s user interface.

LangChain powers the retrieval-augmented generation (RAG).

FAISS provides fast vector search for report content.

PyPDF2 handles PDF text extraction.

🙏 Acknowledgments

Built during an in-house hackathon in 4 hours.
Special thanks to mentors and teammates for feedback during development.

📄 License

This project is licensed under the MIT License.

Author:
Azaan Latif
