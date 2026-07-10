from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class InputState(TypedDict):
    name:str

class OverallState(TypedDict):
    name:str
    greeting_msg:str

class PrivateState(TypedDict):
    final_private_msg:str

class OutputState(TypedDict):
    final_msg:str


# Node1 - create greeting message
def node1(state:InputState)->OverallState:
    greeting_added= "Hello" + state["name"]
    state["greeting_msg"]=greeting_added
    return state

# Node2- add welcome message
def node2(state:OverallState)->PrivateState:
    add_welcome=state["greeting_msg"]+" welcome to Langgraph!"
    state["final_private_msg"]=add_welcome
    return state

# Node3- final message creation
def node3(state:PrivateState)->OutputState:
    final_msg=state["final_private_msg"] + " How are you?"
    state["final_msg"]=final_msg
    return state

builder = StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)

builder.add_node("node1",node1)
builder.add_node("node2",node2)
builder.add_node("node3",node3)

builder.add_edge(START,"node1")
builder.add_edge("node1","node2")
builder.add_edge("node2","node3")
builder.add_edge("node3",END)

graph=builder.compile()

result=graph.invoke({
    "name":" Gayatri"
})

print(result)