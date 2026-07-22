from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
# for coditional routing 
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini")

# here we create multiplication tool
def multiply(a,b):
    """ Multiply two numbers."""
    return a*b

# bind that tool with llm for response
llm_with_tool = llm.bind_tools([multiply])

# Node :  to call llm with tools bound
def tool_calling_node(state:MessagesState):
    """ Node that calls the LLM with tools bound. """
    return {"messages":[llm_with_tool.invoke(state["messages"])]}

# Workflow : 
workflow = StateGraph(MessagesState)
workflow.add_node("tool_calling_node",tool_calling_node)
workflow.add_node("tools",ToolNode([multiply])) # tool node for handling tool calling

workflow.add_conditional_edges("tool_calling_node",tools_condition) # condition to decide that the tool should be call or not

workflow.add_edge(START,"tool_calling_node")
workflow.add_edge("tool_calling_node",END)

app = workflow.compile()

def interact_agent():
    user_input = {"messages":[("human","multiply 50 and 2")]}
    result = app.invoke(user_input)
    return result["messages"][-1].pretty_print()

print(interact_agent())