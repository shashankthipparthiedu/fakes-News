from flask import Flask, render_template, request
import anthropic
import os
from dotenv import load_dotenv  # Import dotenv
 # Debugging line


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("API key not found! Make sure to set ANTHROPIC_API_KEY in the .env file.")

# Initialize the Anthropics API client with the API key
client = anthropic.Anthropic(api_key=api_key)

# Function to label output
def output_label(n):
    return "Not Fake News" if n == 1 else "Fake News"

# Function to check news validity using AI
def check_fact(news_statement):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "assistant", "content": "I'd like to fact-check a news statement. Please verify the following statement:"},
            {"role": "assistant", "content": news_statement},
            {"role": "user", "content": "Is this statement true or false?"}
        ]
    )

    result = str(message.content).strip().lower()
    return 1 if "true" in result else 0

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        news_statement = request.form.get("news_statement")

        if news_statement:
            fact_check_result = check_fact(news_statement)

            # Mimicking different model outputs
            pred_LR = fact_check_result
            pred_DT = fact_check_result
            pred_GB = fact_check_result
            pred_RF = fact_check_result

            result = {
                "LR": output_label(pred_LR),
                "DT": output_label(pred_DT),
                "GBC": output_label(pred_GB),
                "RFC": output_label(pred_RF),
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
