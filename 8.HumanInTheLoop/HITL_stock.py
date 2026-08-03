import os
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState,START,END,StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from dotenv import load_dotenv
load_dotenv()
import finnhub

finnhub_client = finnhub.Client(api_key="d9k78h1r01qkjjrsa8ogd9k78h1r01qkjjrsa8p0")

@tool
def get_stock_price(symbol:str): # here symbol means symbol of companies in stock
    """Retrieve the latest stock price for the given symbol."""
    quote = finnhub_client.quote(symbol)
    return f"The current price for {symbol} is ${quote['c']}."

tool_node=ToolNode([get_stock_price])

llm = ChatOpenAI(model="gpt-4o-mini")
model = llm.bind_tools([get_stock_price])

def agent_reasoning(state:MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages":[response]}

def should_continue(state:MessagesState):
    messages =state["messages"]
    last_msg = messages[-1]
    if not last_msg.tool_calls:
        return "end"
    else:
        return "continue"

# Workflow:

workflow = StateGraph(MessagesState)

workflow.add_node("agent_reasoning",agent_reasoning)
workflow.add_node("tool_node",tool_node)

workflow.add_edge(START,"agent_reasoning")
workflow.add_conditional_edges("agent_reasoning",should_continue,{
    "continue":"tool_node",
    "end":END
})
workflow.add_edge("tool_node","agent_reasoning")

# memory
memory= MemorySaver()
app = workflow.compile(checkpointer=memory,interrupt_before=["tool_node"])

# initial input
initial_input ={"messages":[{"role":"user","content":"Should i buy AAPL stock today"}]}
thread = {"configurable":{"thread_id":"1"}}

for event in app.stream(initial_input,thread,stream_mode="values"):
    print(event)

user_approval = input("Do you approve querying the stock price for APPL ? (yes/no):")

if user_approval.lower() =="yes":
    for event in app.stream(None,thread,stream_mode="values"):
        print(event)
else:
    print("Execution halted by user.")