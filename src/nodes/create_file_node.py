from src.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict
import os
import re
from datetime import datetime
from langchain_groq import ChatGroq
import json

class TaskOutput(BaseModel):
    list_of_tasks: List[str]

from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))

def create_steps(state: AgentState):
    print("inside create_steps node")

    prompt = ChatPromptTemplate.from_template(
        """
        You are an help full assistent in breaking a task in list of task.
        Example:Create a python with retry function.
                you should return a list of task as: ['create python file', "write retry function in created file."]
        
        STRICT RULES:
            - No explanation
            - No text
            - Only list
            - double quotes required
        
        {input}

        """)
    chain = prompt | llm

    response = chain.invoke({
        "input": state["input"]
    })

    print("RAW:", response.content)

    try:
        parsed = json.loads(response.content)
        if isinstance(parsed, list):
            tasks = parsed
        elif isinstance(parsed, dict):
            tasks = parsed.get("list_of_tasks", [])
        else:
            tasks = [response.content]
    except Exception:
        tasks = [response.content]

    print(f"Generated tasks: {tasks}")
    
    return {
    "list_of_tasks": tasks,
    "approved": False,
    "step": "awaiting_confirmation"
    }



def execute_tasks(state):
    print("----------------------------------------------------------------------------")
    print("inside execute")

    tasks = state.get("list_of_tasks") or state.get("list_of_inputs") or []
    if len(tasks) == 1 and isinstance(tasks[0], str):
        try:
            parsed = json.loads(tasks[0])
            if isinstance(parsed, list):
                tasks = parsed
        except Exception:
            pass

    if not isinstance(tasks, list):
        tasks = [str(tasks)]

    print(f'STATE: {tasks}')
    print(f"Executing tasks: {tasks}")

    original_request = ""
    for msg in reversed(state.get("messages", [])):
        text = msg.get("text", "")
        if text.strip().lower() not in {"ok", "yes", "sure", "yep", "confirm"}:
            original_request = text
            break

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "create_files"))
    os.makedirs(output_dir, exist_ok=True)

    user_lower = original_request.lower() if original_request else state.get("input", "").lower()
    if "java" in user_lower:
        file_name = "Generated.java"
    elif "c++" in user_lower or "cpp" in user_lower:
        file_name = "Generated.cpp"
    elif "javascript" in user_lower or "js" in user_lower:
        file_name = "generated.js"
    elif "typescript" in user_lower or "ts" in user_lower:
        file_name = "generated.ts"
    elif "html" in user_lower:
        file_name = "generated.html"
    else:
        file_name = "generated.py"

    file_path = os.path.join(output_dir, file_name)

    prompt = ChatPromptTemplate.from_template(
        """
        You are a code generation assistant.
        Generate only the source code for the requested file, with no markdown fences, no comments about the result, and no extra text.

        Original user request: {original_request}
        Task list:
        {task_list}
        Target filename: {file_name}
        """)
    chain = prompt | llm

    response = chain.invoke({
        "original_request": original_request,
        "task_list": "\n".join(f"- {task}" for task in tasks),
        "file_name": file_name,
    })

    code = response.content.strip()
    if code.startswith("```"):
        code = code.split("```", 2)[1].strip()
    elif "```" in code:
        code = code.replace("```", "").strip()

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Wrote file: {file_path}")
    print("----------------------------------------------------------------------------")

    return {
        "file_path": file_path,
        "code": code,
        "step": "done"
    }