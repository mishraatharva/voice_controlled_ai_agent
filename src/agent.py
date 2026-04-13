from langgraph.graph import StateGraph, END
from src.nodes.intent_node import detect_intent
from src.nodes.create_file_node import create_steps, execute_tasks
from src.state import AgentState

def router(state):

    user_input = state.get("input", "").lower()

    # if user says ok → execute
    if user_input in ["ok", "yes"]:
        return "execute_tasks"

    # otherwise → create steps
    if state.get("intent") == "create_file":
        return "create_steps"


graph = StateGraph(AgentState)

graph.add_node("intent", detect_intent)
graph.add_node("create_steps", create_steps)
graph.add_node("execute_tasks", execute_tasks)

graph.set_entry_point("intent")

graph.add_conditional_edges("intent", router, {
    "create_steps": "create_steps",
    "execute_tasks": "execute_tasks"
})

# STOP after steps
graph.add_edge("create_steps", END)

graph.add_edge("execute_tasks", END)


def return_bot():
    return graph.compile()