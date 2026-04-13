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

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant in classifying user intents. 
    Classify the user's intent into one of the following categories:
    
    - create_file
    - edit_code
    - other
    
    Rules:
    If asked to create file → create_file
    If asked to edit code → edit_code
    Else → other

    User: {input}
    """)

    structured_llm = llm.with_structured_output(IntentOutput)

    formatted_prompt = prompt.invoke({
        "input": state["input"]
    })

    result = structured_llm.invoke(formatted_prompt)

    user_message = {"role": "user", "text": state["input"]}
    current_messages = state.get("messages", [])

    print(f"Detected intent: {result.intent}")

    return {
        "intent": result.intent,
        "messages": current_messages + [user_message]
    }