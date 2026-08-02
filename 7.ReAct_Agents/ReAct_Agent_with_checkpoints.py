# import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.runnables.graph import MermaidDrawMethod, CurveStyle
from dotenv import load_dotenv
load_dotenv()

# Tool
def product_info(product_name:str)->str:
    """Fetch product information."""
    product_catalog = {
        "iphone 20" : "The latest features an A15 chip and improved camera.",
        "Macbook" : "The new macbook has m2 chip and a 14-inch Retina display." }
    return product_catalog.get(product_name.lower(),"Product not found")

# object of ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# object of MemorySaver
checkpointer = MemorySaver()

# Create ReAct agent 
graph = create_react_agent(model=llm,tools=[product_info],checkpointer=checkpointer) # here we give our tool in '[]' bcoz there is list of tool if only one tool for ex; only addition is there then we give it simply without []

# for thread configration to simulate single threaded memory
config = {"configurable":{"thread_id":"thread-1"}}
## here we used cofig for graph setting with single thread id so it can store all info in single thread it and its easy for agent to remeber the past also


# user input 

inputs = {"messages":[("human","Hi, I'm Gayatri.Tell me about the new iPhone 20.")]}
messages = graph.invoke(inputs,config)
for message in messages["messages"]:
    message.pretty_print()

inputs2 = {"messages":[("human","Tell me more about the iPhone 20.")]}
messages2 = graph.invoke(inputs2,config)
for message in messages2["messages"]:
    message.pretty_print()


