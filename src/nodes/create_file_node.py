from src.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import TypedDict, List, Dict
import os
from langchain_groq import ChatGroq
import json

class TaskOutput(BaseModel):
    list_of_tasks: List[str]

from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))

def create_file(state: AgentState):
    print("inside create file node")
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
        tasks = parsed.get("list_of_tasks", [])
    except:
        tasks = [response.content]

    print(f"Generated tasks: {tasks[0]}")
    
    return {
    "list_of_tasks": tasks,
    "approved": False,
    "step": "awaiting_confirmation"
    }


def confirm_tasks(state: AgentState):
    tasks = state["list_of_tasks"]

    # Format nicely for UI
    formatted = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])

    return {
        "confirmation_message": f"Please confirm the tasks:\n{formatted}"
    }


def modify_tasks(state: AgentState):
    feedback = state.get("user_feedback", "")

    prompt = ChatPromptTemplate.from_template("""
    Update the task_list based on user feedback: {feedback}
    task_list: {list_of_tasks}
    """)

    structured_llm = llm.with_structured_output(TaskOutput)

    response = structured_llm.invoke({
        "feedback": feedback,
        "list_of_tasks": state["list_of_tasks"]
    })

    return {
        "list_of_tasks": response.list_of_tasks,
        "approved": False
    }


def execute_tasks(state: AgentState):
    tasks = state["list_of_tasks"]

    for task in tasks:
        print(f"Executing: {task}")
        # your actual logic here

    return {"status": "completed"}