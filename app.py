from flask import Flask, render_template, request
import anthropic
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("API key not found! Make sure to set ANTHROPIC_API_KEY in the .env file.")

# Initialize the AI client
client = anthropic.Anthropic(api_key=api_key)

def output_label(n):
    return "Not Fake News" if n == 1 else "Fake News"

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
            result = {
                "LR": output_label(fact_check_result),
                "DT": output_label(fact_check_result),
                "GBC": output_label(fact_check_result),
                "RFC": output_label(fact_check_result),
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
