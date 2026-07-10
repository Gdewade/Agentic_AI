from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class addition_state(TypedDict):
    a:int
    b:int
    result:int

def node1(state:addition_state):
    state["result"] = state["a"] + state["b"]
    return state

builder = StateGraph(addition_state)
builder.add_node("node1",node1)
builder.add_edge(START,"node1")
builder.add_edge("node1",END)

graph = builder.compile()

num1=int(input("Enter 1st number :"))
num2=int(input("Enter 2nd number :"))

result = graph.invoke({
    "a":num1,
    "b":num2,
    "result":0
})

print(result)


