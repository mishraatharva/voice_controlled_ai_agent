from flask import Flask, render_template, request, jsonify
from src.agent import return_bot
from dotenv import load_dotenv
 
load_dotenv()
app = Flask(__name__)

session_state = {
    "input": "",
    "intent": "",
    "list_of_tasks": [],
    "approved": False,
    "user_feedback": "",
    "messages": [],
    "step" : "start"
}

bot = return_bot()

# -------------------------------
# LOAD UI PAGE,
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")  # your HTML file


# -------------------------------
#  CHAT ROUTE (ALL LOGIC)
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    global session_state

    data = request.json

    message = data.get("message")
    approved = data.get("approved", False)
    feedback = data.get("feedback", "")

    # ---------------------------
    # NEW MESSAGE
    # ---------------------------
    if message:
        session_state["input"] = message
        session_state["approved"] = False
        session_state["user_feedback"] = ""
        session_state["step"] = "start"

        result = bot.invoke(session_state)
        session_state.update(result)

        return jsonify({
            "tasks": result.get("confirmation_message")
        })

    # ---------------------------
    # APPROVE
    # ---------------------------
    if approved:
        session_state["approved"] = True
        session_state["step"] = "execute"

        result = bot.invoke(session_state)
        session_state.update(result)

        # 🔥 reset after execution
        session_state["approved"] = False
        session_state["user_feedback"] = ""
        session_state["step"] = "start"

        return jsonify({
            "file_path": result.get("file_path"),
            "code": result.get("code_content")
        })

    # ---------------------------
    # EDIT
    # ---------------------------
    if feedback:
        session_state["user_feedback"] = feedback
        session_state["approved"] = False
        session_state["step"] = "modify"

        result = bot.invoke(session_state)
        session_state.update(result)

        return jsonify({
            "tasks": result.get("confirmation_message")
        })

    return jsonify({"error": "Invalid request"})


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)