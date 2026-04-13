from flask import Flask, render_template, request, jsonify
from src.agent import return_bot
from dotenv import load_dotenv
 
load_dotenv()
app = Flask(__name__)

session_state = {
    "input": "",
    "intent": "",
    "list_of_tasks": [],
    "step": ""
}

bot = return_bot()

from src.state import AgentState
from langchain_core.prompts import ChatPromptTemplate

# -------------------------------
# LOAD UI PAGE,
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global session_state 

    data = request.json
    message = data.get("message")
    print(f"Received message: {message}")
    session_state["input"] = message

    result = bot.invoke(session_state)

    session_state.update(result)

    return jsonify({
        "tasks": result.get("list_of_tasks")
    })


if __name__ == "__main__":
    app.run(debug=True)