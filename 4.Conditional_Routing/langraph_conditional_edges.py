from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END

class GreetingState(TypedDict):
    greeting:str

# convert user input into lowercase
def node1(state:GreetingState):
    state['greeting'] = state['greeting'].lower()
    return state

def node2(state:GreetingState):
    state['greeting'] = state['greeting'] + ", welcome to langchain"
    return state

def node3(state:GreetingState):
    state['greeting'] = state['greeting'] + ", welcome to langgraph"
    return state

# this is conditional node
def node4(state:GreetingState):
    if "good morning" in state['greeting']:
        return "node2"
    else:
        return "node3"
    


builder = StateGraph(GreetingState,input_schema=GreetingState,output_schema=GreetingState)

builder.add_node("node1",node1)
builder.add_node("node2",node2)
builder.add_node("node3",node3)
builder.add_node("node4",node4)

builder.add_edge(START,"node1")
builder.add_conditional_edges("node1",node4)
builder.add_edge("node2",END)
builder.add_edge("node3",END)

graph = builder.compile()

user_input = input("Enter a greeting message : ")
result = graph.invoke({
    "greeting":user_input
})

print(result)