from flask import Flask, render_template, request, jsonify
from src.agent import return_bot
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import os
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

# @app.route("/chat", methods=["POST"])
# def chat():
#     global session_state 

#     data = request.json
#     message = data.get("message")
#     print(f"Received message: {message}")
#     session_state["input"] = message

#     result = bot.invoke(session_state)

#     session_state.update(result)

#     return jsonify({
#         "tasks": result.get("list_of_tasks")
#     })
@app.route("/chat", methods=["POST"])
def chat():
    global session_state 

    message = None

    # 1. If JSON (normal text)
    if request.is_json:
        data = request.json
        message = data.get("message")

    # 2. If audio file comes
    elif "audio" in request.files:
        audio_file = request.files["audio"]

        from pydub import AudioSegment
        import speech_recognition as sr
        import tempfile

        try:
            # 🔥 save temp webm
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
                audio_file.save(temp_audio.name)

                # 🔥 convert webm → wav
                sound = AudioSegment.from_file(temp_audio.name)
                wav_path = temp_audio.name.replace(".webm", ".wav")
                sound.export(wav_path, format="wav")

            recognizer = sr.Recognizer()

            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)

            message = recognizer.recognize_google(audio)

        except Exception as e:
            print("Audio error:", e)
            return jsonify({"error": "Could not process audio"})

    print(f"Received message: {message}")

    if not message:
        return jsonify({"error": "No input received"})

    session_state["input"] = message

    result = bot.invoke(session_state)

    session_state.update(result)

    return jsonify({
        "message": message,
        "tasks": result.get("list_of_tasks")
    })


if __name__ == "__main__":
    app.run(debug=True)