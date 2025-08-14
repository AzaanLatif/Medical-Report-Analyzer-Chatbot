# chat.py

from retriever import create_retriever
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

def create_chatbot():
    # Initialize retriever from retriever.py
    retriever = create_retriever()

    # LLM configuration
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Fast + cheaper model; can change to gpt-4o
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Retrieval-based QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def get_answer(retriever, query):
    """Get answer from the medical report with improved context and helpful responses."""
    # Create a more specific prompt that encourages detailed, helpful answers
    prompt_template = """You are a helpful medical assistant explaining a medical report. 
    Use the following context to answer the question. If you're not sure about something, explain what you do know from the context
    and suggest what kind of medical professional they should consult for more specific advice.
    
    Context: {context}
    
    Question: {question}
    
Provide a clear answer in a helpful and easy-to-understand way. If the question is about medical advice,
always remind the user to consult with their healthcare provider for personalized medical guidance.
Additionally, do not answer anything which is not in context to the report."""

    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Create the QA chain with the custom prompt
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PromptTemplate(
                    template=prompt_template,
                    input_variables=["context", "question"]
                ),
            }
        )
        
        # Get the response
        response = qa_chain.invoke({"query": query})
        
        # If no specific answer found, provide a helpful fallback response
        if "I don't know" in response["result"] or not response["result"].strip():
            return """Based on the medical report, I cannot find a specific answer to your question. 
            However, this is an important question that you should discuss with your healthcare provider. 
            They can provide personalized advice based on your complete medical history."""
            
        return response["result"]
        
    except Exception as e:
        print(f"Error in get_answer: {str(e)}")  # For debugging
        return "I apologize, but I encountered an error processing your question. Please try rephrasing your question or ask something else about the medical report."

def generate_summary(retriever):
    """Generate a patient-friendly summary of the medical report."""
    prompt = """ Please Summarize the medical report in a clear, patient-friendly way. Show the patients name, key findings with simple explanations,
    explain what they mean, suggest the right type of doctor to visit, and give a safe, general diet & lifestyle plan.









Ask ChatGPT
"""
    
    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )
        
        response = qa_chain.invoke({"query": prompt})
        return response["result"]
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def chat_with_report():
    print("🩺 Medical Report Chatbot — Ask questions about your uploaded report!")
    print("Type 'exit' to quit.\n")

    qa_chain = create_chatbot()

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye! 🩺")
            break
        try:
            response = qa_chain.invoke({"query": query})
            print("\nBot:", response["result"], "\n")
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    chat_with_report()
