import gradio as gr
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL
BACKEND_URL = "http://localhost:5000/solve"

def math_chatbot(query, user):
    """Handle math queries by sending them to the backend"""
    try:
        logger.info(f"Processing query: {query} from user: {user}")

        if not query.strip():
            return "Please enter a math problem."

        # Send request to backend
        response = requests.post(
            BACKEND_URL,
            json={"question": query, "user": user},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            return f"Answer: {result['answer']}"
        else:
            error_msg = response.json().get('error', 'Unknown error occurred')
            logger.error(f"Backend error: {error_msg}")
            return f"Error: {error_msg}"

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {str(e)}")
        return "Error: Could not connect to the backend server. Please check if it's running."
    except Exception as e:
        logger.error(f"Error in math_chatbot: {str(e)}")
        return f"Error: {str(e)}"


# Create enhanced interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Math Chatbot")
        gr.Markdown("Ask me any math problem! I can help with basic arithmetic, derivatives, integrals, and more.")

        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(label="Enter your math problem", placeholder="e.g., integrate x^2 dx", lines=2)
                user_input = gr.Textbox(label="Your Name", placeholder="Enter your name", value="Anonymous")
                submit_button = gr.Button("Submit")
            with gr.Column():
                output = gr.Textbox(label="Solution", interactive=False)

        gr.Examples(
            examples=[
                ["integrate x^2 dx", "Alice"],
                ["derivative of sin(x)", "Bob"],
                ["solve x^2 + 2x + 1 = 0", "Charlie"],
            ],
            inputs=[query_input, user_input]
        )

        submit_button.click(fn=math_chatbot, inputs=[query_input, user_input], outputs=output)

    return demo


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_port=7860)