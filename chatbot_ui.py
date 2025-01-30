# chatbot_ui.py
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
        response = requests.post(BACKEND_URL,
                                 json={"question": query, "user": user},
                                 timeout=10)

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


# Create interface
def create_interface():
    return gr.Interface(
        fn=math_chatbot,
        inputs=[
            gr.Textbox(label="Enter your math problem", placeholder="e.g., 2 + 2"),
            gr.Textbox(label="Your Name", placeholder="Enter your name", value="Anonymous")
        ],
        outputs=gr.Textbox(label="Solution"),
        title="AI Math Chatbot",
        description="Ask me any math problem! I can help with basic calculations.",
        examples=[
            ["2 + 2", "StudentA"],
            ["10 * 5", "StudentB"],
        ]
    )


if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_port=7860)