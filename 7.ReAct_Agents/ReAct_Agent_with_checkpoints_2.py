import os
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()

def product_info(product_name:str)->str:
    """Fetch product information"""
    product_catalog = {
        "iPhone":"The latest iPhone features an A15 chip and imporved camera",
        "MacBook":"The new MacBook has an M2 chip and a 14-inch Retina display"
    }
    return product_catalog.get(product_name,"Sorry,product not found.")

def check_stock(product_name:str)->str:
    """Check product stock availability"""
    stock_data={
        "iPhone":"In stock",
        "MacBook":"Out of stock"
    }
    return stock_data.get(product_name,"Stock information unavailable.")

# object of ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# Object of MemorySaver
checkpointer = MemorySaver()

# react agent
graph = create_react_agent(model=llm,tools=[product_info,check_stock],checkpointer=checkpointer)

# configuration for single thread memory
config={"configurable":{"thread_id":"thread-1"}}

# user inputs

input1={"messages":[("human","Tell me about the new iPhone")]}
messages = graph.invoke(input1,config)
for message in messages["messages"]:
    message.pretty_print()

input2={"messages":[("human","Is the iPhone in stock ?")]}
messages2 = graph.invoke(input2,config)
for message in messages2["messages"]:
    message.pretty_print()


