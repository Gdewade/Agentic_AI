from langgraph.graph import StateGraph, MessagesState, START, END
import requests
import urllib

# node : to fetch live calculator

def calculator(state:MessagesState):

    user_query = state["messages"][-1].content
    expression = user_query.split("calculate")[-1].strip() # extract arthmetic expression from user query
    encoded_expression = urllib.parse.quote(expression) # URL-encode the expression to ensure its safe to user in the query string
    print("Encoded Expression ----> ",encoded_expression)

    url = f"http://api.mathjs.org/v4/?expr={encoded_expression}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        result = response.text
        print("result --->",result)
        return {"messages":[f"The result of {expression} is {result}."]}
    else:
        return {"messages":["Sorry, I couldn't calculate that."]}


# workflow:

workflow = StateGraph(MessagesState)

workflow.add_node("calculator",calculator)

workflow.add_edge(START,"calculator")
workflow.add_edge("calculator",END)

app = workflow.compile()

def interact_agent():

    input_msg = {"messages":[("human","calculate 31+05+2005")]}
    for result in app.stream(input_msg,stream_mode="values"):
        result["messages"][-1].pretty_print()

interact_agent()




