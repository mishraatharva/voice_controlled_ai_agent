# Voice-Controlled Local AI Agent

A modular Python project for a voice-controlled local AI agent with LangGraph-style state management, Groq LLM integration, Whisper STT, and a Gradio user interface.

## Project Structure

- `app/main.py` - Launches the Gradio interface.
- `app/agent.py` - Workflow orchestration and node execution.
- `app/state.py` - Strongly typed state object for session flow.
- `app/tools.py` - Safe file operations and summarization helpers.
- `app/ui.py` - Gradio UI wiring and confirmation flow.
- `app/memory.py` - Optional session persistence in `output/memory/`.
- `output/` - Local workspace for generated files and persisted session memory.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Then copy `.env.example` to `.env` and set your `GROQ_API_KEY`.

## Run the App

```bash
python -m app.main
```

Open the Gradio link in your browser. You can speak through the microphone, upload an audio file, or type a command.

## Features

- Uses structured `AgentState` across nodes.
- Maintains `chat_history` for follow-up commands.
- Supports audio STT via local Whisper.
- Classifies intent and extracts entities.
- Generates planned actions and requires confirmation for file writes.
- Executes file creation under `./output/` only.
- Allows modification flow before execution.
- Persists session memory as JSON per session.

## Notes

- `GROQ_API_KEY` is required for remote LLM intent classification and chat generation.
- If no API key is provided, the agent falls back to a simple local intent classifier.
- File operations are restricted to `./output/` for safety.
