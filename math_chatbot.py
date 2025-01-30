import json
import datetime
import logging
import sympy
import re
from sympy import symbols, solve, diff, integrate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUERIES_FILE = "queries.json"


def solve_math_problem(question):
    """
    Solve various types of math problems including:
    - Basic arithmetic
    - Quadratic equations
    - Derivatives
    - Integrals
    """
    try:
        question = question.lower().strip()
        x = symbols('x')

        # Handle derivatives
        if 'derivative' in question or 'differentiate' in question:
            # Extract the expression after "derivative of" or "differentiate"
            expr_str = re.split(r'derivative of|differentiate', question)[-1].strip()
            expr = sympy.sympify(expr_str)
            result = diff(expr, x)
            return f"The derivative of {expr} is: {result}"

        # Handle integrals
        elif 'integral' in question or 'integrate' in question:
            # Extract the expression after "integral of" or "integrate"
            expr_str = re.split(r'integral of|integrate', question)[-1].strip()
            expr = sympy.sympify(expr_str)
            result = integrate(expr, x)
            return f"The integral of {expr} is: {result} + C"

        # Handle quadratic equations
        elif 'solve' in question and ('x^2' in question or 'x**2' in question):
            # Clean up the equation
            eq_str = question.replace('solve', '').replace('equation', '').strip()
            if '=' in eq_str:
                left, right = eq_str.split('=')
                eq_str = f"({left}) - ({right})"
            expr = sympy.sympify(eq_str)
            solutions = solve(expr, x)
            return f"The solutions are: {solutions}"

        # Handle basic arithmetic
        else:
            # Remove any non-math characters for basic arithmetic
            cleaned_question = ''.join(c for c in question if c.isdigit() or c in '+-*/(). ')
            if cleaned_question:
                result = eval(cleaned_question)
                return str(result)

        return "Could not process the math problem. Please check the format."

    except Exception as e:
        logger.error(f"Error solving problem: {str(e)}")
        return f"Error: Please check the format of your mathematical expression. Error details: {str(e)}"


def store_query(user, question, answer):
    """Store queries in JSON file with error handling"""
    try:
        # Load existing queries
        try:
            with open(QUERIES_FILE, "r") as file:
                queries = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            queries = []

        # Add the new query
        queries.append({
            "user": user,
            "question": question,
            "answer": answer,
            "timestamp": str(datetime.datetime.now())
        })

        # Save the updated queries
        with open(QUERIES_FILE, "w") as file:
            json.dump(queries, file, indent=4)

    except Exception as e:
        logger.error(f"Error storing query: {str(e)}")


if __name__ == "__main__":
    # Test cases
    test_cases = [
        "2 + 2",
        "derivative of x^2 + 3x + 5",
        "integrate x^2 + 2x",
        "solve x^2 + 2x + 1 = 0"
    ]

    for test in test_cases:
        print(f"\nTesting: {test}")
        print(f"Result: {solve_math_problem(test)}")