#app.py
from flask import Flask, render_template, request
import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Set your API key
os.environ["OPENROUTER_API_KEY"] = "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"

# Initialize model
model = init_chat_model(
    "auto",
    model_provider="openrouter",
    temperature=0.2
)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""

    if request.method == "POST":
        role = request.form.get("role")
        topic = request.form.get("topic")

        prompt = ChatPromptTemplate.from_template(
            "You are a {role}. Explain the concept of {topic} in one paragraph."
        )

        messages = prompt.format_prompt(role=role, topic=topic).to_messages()
        result = model.invoke(messages)

        response = result.content

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
