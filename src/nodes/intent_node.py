import os
import json
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from src.prompts.detect_intent_prompt import DETECT_INTENT_PROMPT
from src.state import AgentState
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from dotenv import load_dotenv
 
load_dotenv()


llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))


class IntentOutput(BaseModel):
    intent: str


def detect_intent(state: AgentState):
    print("inside intent node")
    print(state)

    user_input = state.get("input", "").strip().lower()
    if state.get("step") == "awaiting_confirmation" and user_input in {"ok", "yes", "sure", "yep", "confirm"}:
        print("Skipping intent LLM for confirmation reply")
        return {"intent": state.get("intent", "create_file")}

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant in classifying user intents. 
    Classify the user's intent into one of the following categories:
    
    - create_file
    - other
    
    Rules:
    If asked to create file → create_file
    If asked anything else → other
    
    User: {input}
    """)

    structured_llm = llm.with_structured_output(IntentOutput)

    formatted_prompt = prompt.invoke({
        "input": state.get("input", "")
    })

    result = structured_llm.invoke(formatted_prompt)

    user_message = {"role": "user", "text": state["input"]}
    current_messages = state.get("messages", [])

    print(f"Detected intent: {result.intent}")

    return {
        "intent": result.intent,
        "messages": current_messages + [user_message]
    }