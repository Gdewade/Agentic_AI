import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent # it is prebuilt class in langgraph for Reason and Action agent
from display_graph import display_graph
from dotenv import load_dotenv
load_dotenv()

# Define tools 

def add(a,b):
    """Add two numbers together"""
    return a+b

def multiply(a,b):
    """"Multiply two numbers together"""
    return a*b

def divide(a,b):
    """Divide a and b
    Args:
        a: first int
        b: second int """

    return a/b

tools = [add,multiply,divide]

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o-mini")

# Create the ReAct Agent
graph = create_react_agent(model = llm, tools=tools)

#Visualize the graph
display_graph(graph,file_name = os.path.basename(__file__))

# user input
inputs = {"messages":[("Human","multiply 2 and 3 and add this result to 10")]}

# Run the react agent
messages = graph.invoke(inputs)

for message in messages["messages"]:
    message.pretty_print()