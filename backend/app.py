print("Starting Gradio app...")  # Add this at the top

import gradio as gr
from loader import process_pdf
from retriever import create_retriever
from chat import get_answer, generate_summary

# Global variables
retriever = None
summary = None

def upload_pdf(file):
    global retriever
    if file is None:
        return "Please select a PDF file first."
    process_pdf(file.name)
    retriever = create_retriever()
    return "✨ Medical report processed successfully"

def create_summary():
    global retriever, summary
    if retriever is None:
        return "⚠️ Please upload a medical report first."
    summary = generate_summary(retriever)
    return summary

def ask_question(query):
    global retriever, summary
    if retriever is None:
        return "⚠️ Please upload a medical report first."
    if summary is None:
        return "⚠️ Please generate a summary first."
    if not query.strip():
        return "⚠️ Please enter a question."
    return get_answer(retriever, query)

# Custom CSS for modern, professional styling with gradients
custom_css = """
#component-0 {
    max-width: 880px;
    margin: auto;
    padding: 0 20px;
}
.contain {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.18);
}
.header {
    text-align: center;
    margin-bottom: 30px;
    background: linear-gradient(120deg, #1a2980, #26d0ce);
    margin: -30px -30px 30px -30px;
    padding: 40px 20px;
    border-radius: 20px 20px 0 0;
}
.header h1 {
    font-size: 2.5rem !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 10px !important;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}
.header p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.1rem !important;
}
.upload-box {
    border: 2px dashed rgba(26, 41, 128, 0.3);
    border-radius: 12px;
    padding: 20px;
    background: linear-gradient(145deg, #f0f7ff, #ffffff);
    text-align: center;
    transition: all 0.3s ease;
}
.upload-box:hover {
    border-color: #26d0ce;
    box-shadow: 0 4px 15px rgba(38, 208, 206, 0.1);
}
.btn {
    background: linear-gradient(45deg, #1a2980, #26d0ce) !important;
    border: none !important;
    color: white !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2) !important;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(26, 41, 128, 0.2) !important;
}
.output-box {
    border: 1px solid rgba(26, 41, 128, 0.1);
    border-radius: 12px;
    padding: 15px;
    background: linear-gradient(145deg, #ffffff, #f0f7ff);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}
.disclaimer {
    margin-top: 20px;
    padding: 15px;
    background: linear-gradient(to right, #fff5f5, #ffe8e8);
    border-left: 4px solid #1a2980;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #4A5568;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
"""

# Create custom theme with gradient background
theme = gr.themes.Soft().set(
    body_background_fill="linear-gradient(135deg, #1a2980 0%, #26d0ce 100%)",
    button_primary_background_fill="linear-gradient(45deg, #1a2980, #26d0ce)",
    button_primary_background_fill_hover="linear-gradient(45deg, #26d0ce, #1a2980)",
    button_secondary_background_fill="linear-gradient(45deg, #4A5568, #718096)",
    button_secondary_background_fill_hover="linear-gradient(45deg, #718096, #4A5568)",
    input_background_fill="#241d1d",
    block_background_fill="rgba(255, 255, 255, 0.95)",
    block_border_width="0px",
)

# Gradio interface
with gr.Blocks(theme=theme, css=custom_css) as demo:
    with gr.Column(elem_classes="contain"):
        # Header
        with gr.Column(elem_classes="header"):
            gr.Markdown(
                """
                # 🏥 Medical Report Assistant
                Understand your medical reports with ease
                """
            )
        
        # Main Content
        with gr.Column():
            # Upload Section
            with gr.Column(elem_classes="upload-box"):
                with gr.Row():
                    pdf_input = gr.File(
                        label="Upload Medical Report",
                        type="filepath",
                        file_types=[".pdf"],
                    )
                with gr.Row():
                    upload_button = gr.Button("Process Report", elem_classes="btn")
                    summary_button = gr.Button("Generate Summary", elem_classes="btn")
                status_output = gr.Textbox(
                    show_label=False,
                    interactive=False,
                    elem_classes="output-box"
                )
            
            # Summary Section
            summary_output = gr.Textbox(
                label="Report Summary",
                lines=6,
                interactive=False,
                elem_classes="output-box"
            )
            
            # Q&A Section
            with gr.Row():
                question_input = gr.Textbox(
                    label="Ask a Question",
                    placeholder="Example: What are the main findings in my report?",
                    lines=2
                )
            with gr.Row():
                ask_button = gr.Button("Get Answer", elem_classes="btn")
            answer_output = gr.Textbox(
                label="Answer",
                lines=4,
                interactive=False,
                elem_classes="output-box"
            )
            
            # Disclaimer
            gr.Markdown(
                """
                <div class="disclaimer">
                    <strong>Important Notice:</strong><br>
                    This tool provides general information only and should not replace professional medical advice. 
                    Always consult with your healthcare provider for medical decisions.
                </div>
                """
            )
        
        # Event Handlers
        upload_button.click(
            fn=upload_pdf,
            inputs=[pdf_input],
            outputs=status_output,
            show_progress=True
        )
        
        summary_button.click(
            fn=create_summary,
            inputs=[],
            outputs=summary_output,
            show_progress=True
        )
        
        ask_button.click(
            fn=ask_question,
            inputs=[question_input],
            outputs=answer_output,
            show_progress=True
        )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860
    )
