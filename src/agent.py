from langgraph.graph import StateGraph, END
from src.nodes.intent_node import detect_intent
from src.nodes.create_file_node import create_file, confirm_tasks, modify_tasks, execute_tasks
from src.nodes.edit_file_node import edit_file
from src.state import AgentState

def router(state: AgentState):
    if state["intent"] == "create_file":
        return "create_file"

    if state["intent"] == "edit_file":
        return "edit_file"


def approval_router(state: AgentState):
    
    #WAIT here — do nothing
    if state.get("step") == "awaiting_confirmation":
        return "end" 

    # user clicked approve
    if state.get("approved"):
        return "execute_tasks"

    # user gave feedback
    if state.get("user_feedback"):
        return "modify_tasks"

    return "end"


graph = StateGraph(AgentState)

graph.add_node("intent", detect_intent)
graph.add_node("create_file", create_file)
graph.add_node("confirm_tasks", confirm_tasks)
graph.add_node("modify_tasks", modify_tasks)
graph.add_node("execute_tasks", execute_tasks)

graph.add_node("edit_file", edit_file)


graph.set_entry_point("intent")

graph.add_conditional_edges("intent", router, {
    "create_file": "create_file",
    "edit_file": "edit_file"
})

graph.add_edge("create_file", "confirm_tasks")

graph.add_conditional_edges(
    "confirm_tasks",
    approval_router,
    {
        "execute_tasks": "execute_tasks",
        "modify_tasks": "modify_tasks",
        "end": END  
    }
)

# IMPORTANT
graph.add_edge("modify_tasks", "confirm_tasks")
graph.add_edge("execute_tasks", END)

# NEW FLOW
# graph.add_edge("create_file", "confirm_tasks")

# graph.add_conditional_edges("confirm_tasks", approval_router, {
#     "execute_tasks": "execute_tasks",
#     "modify_tasks": "modify_tasks"
# })

# graph.add_edge("modify_tasks", "confirm_tasks")
# graph.add_edge("execute_tasks", END)

def return_bot():
    return graph.compile()