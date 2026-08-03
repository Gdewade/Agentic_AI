import os
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver

# State :
class State(TypedDict):
    input:str

# Nodes :
def step_1(state:State):
    print("---step 1---",state["input"])
    return state

def step_2(state:State):
    state["input"] = state["input"] + "can you perform multi-agent systems ?"
    print("---step 2---",state["input"])
    return state

# workflow / graph:

workflow = StateGraph(State)
workflow.add_node("step_1",step_1)
workflow.add_node("step_2",step_2)
workflow.add_edge(START,"step_1")
workflow.add_edge("step_1","step_2")
workflow.add_edge("step_2",END)

# set memory saver and breakpoints
memory = MemorySaver()

graph = workflow.compile(checkpointer=memory,interrupt_before=["step_1"])

config = {"configurable":{"thread_id":"thread-1"}}

initial_input = {"input":"Hello, LangGraph !"}

# for first reading purpose
for event in graph.stream(initial_input,config,stream_mode="values"):
    print(event)

# here they ask user 
user_approval = input("Do you approve to continue to step 2 ? (yes/no):")

# for reading after user response
if user_approval.lower()=="yes":
    for event in graph.stream(None,config,stream_mode="values"):
        print(event)
else:
    print("Execution halted by user.")
