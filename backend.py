# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from math_chatbot import solve_math_problem, store_query

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


@app.route("/solve", methods=["POST"])
def solve():
    """Handle math problem solving requests"""
    try:
        data = request.json
        logger.info(f"Received request: {data}")

        if not data:
            return jsonify({"error": "No data provided"}), 400

        question = data.get("question")
        user = data.get("user", "Anonymous")

        if not question:
            return jsonify({"error": "Please provide a math question"}), 400

        logger.info(f"Processing question: {question}")
        answer = solve_math_problem(question)
        logger.info(f"Generated answer: {answer}")

        # Store the query
        try:
            store_query(user, question, answer)
        except Exception as e:
            logger.warning(f"Failed to store query: {e}")

        return jsonify({
            "question": question,
            "answer": answer
        })

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)