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

def check_fact(news_statement):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"Fact-check the following news statement and return whether it is true or false, along with an explanation: {news_statement}"}
        ]
    )
    
    result = message.content.strip()
    
    if "true" in result.lower():
        return "Not Fake News", result
    else:
        return "Fake News", result

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    explanation = ""
    if request.method == "POST":
        news_statement = request.form.get("news_statement")
        if news_statement:
            result_label, explanation = check_fact(news_statement)
            result = {
                "LR": result_label,
                "DT": result_label,
                "GBC": result_label,
                "RFC": result_label,
                "Explanation": explanation
            }
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
