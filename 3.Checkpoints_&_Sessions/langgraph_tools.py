from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

from dotenv import load_dotenv
load_dotenv()

# Define a tool to fetch weather information
# (its nothing but where we store information of weather)

@tool
def fetch_weather(location:str):
    """
    This tool returns the weather information for a specific location.

    """
    weather_info = {
        "pune":"Its rainy today",
        "mumbai": "Its cloudy today",
        "nashik": "Its sunny today"
    }
    return weather_info.get(location.lower(),"weather info is not available for the provided location")

# create tool node

tool_node = ToolNode([fetch_weather],handle_tool_errors=False)

# merging of llm and tool

llm = ChatOpenAI(model = "gpt-4o-mini").bind_tools([fetch_weather])

# create node

def calling_llm(state:MessagesState):
    msg = state["messages"]
    response = llm.invoke(msg)
    print(response)

    if response.tool_calls:
        tool_result = tool_node.invoke({"messages":[response]})
        # append the total output to the response message
        tool_msg = tool_result["messages"][-1].content
        response.content = response.content + f"\n Tool result : {tool_msg}"
    return {"messages":[response]}

workflow = StateGraph(MessagesState)

workflow.add_node("calling_llm",calling_llm)

workflow.add_edge(START,"calling_llm")
workflow.add_edge("calling_llm",END)

app = workflow.compile()

def interact_agent():
    while True:

        user_input = input("You : ")
        if user_input.lower() in ["exit","quit"]:
            print("Terminated")
            break

        input_variables={
            "messages" : [("human",user_input)]
        }

        for chunk in app.stream(input_variables,stream_mode="values"):
            chunk["messages"][-1].pretty_print()

interact_agent()




