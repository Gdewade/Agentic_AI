from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
import operator

# State :
class State(TypedDict):
    messages:Annotated[list,operator.add]

# node 1 : Weather
def weather(state:State):
    return{"messages":["Its 25°C and sunny."]}

# node 2 : Calculator
def calculator(state:State):
    return{"messages":["2 + 2 equals 4."]}

# workflow :
workflow = StateGraph(State)

workflow.add_node("weather",weather)
workflow.add_node("calculator",calculator)

workflow.add_edge(START,"weather")
workflow.add_edge("weather","calculator")
workflow.add_edge("calculator",END)

app = workflow.compile()

def interact_agent():
    
    input_message = {"messages":[("human","Tell me the weather")]}

    # # full state streaming : give all values as output
    # for result in app.stream(input_message,stream_mode="updates"):
    #     print(result)

    # update streaming : only updated or matching output
    for result in app.stream(input_message,stream_mode="values"):
        print(result)


interact_agent()


