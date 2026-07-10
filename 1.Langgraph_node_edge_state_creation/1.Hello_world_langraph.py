from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

# state
class GreetingState(TypedDict):
    greeting:str

# node
def node1(state:GreetingState):
    state["greeting"] = state["greeting"] + ", How are you"
    return state

# here we create graph
builder = StateGraph(GreetingState) # object of class StateGraph
builder.add_node("node1",node1)
builder.add_edge(START,"node1")
builder.add_edge("node1",END)

graph = builder.compile() # here graph prepares the workflow
result = graph.invoke({
    "greeting":"Good Morning"
})
print(result)

print(graph.get_graph().draw_ascii())