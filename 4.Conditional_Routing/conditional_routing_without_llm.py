from langgraph.graph import StateGraph, START, END, MessagesState

# node1 : weather
def weather(state:MessagesState):
    return{"messages":["It is sunny with a temperature of 25°C."]}

# node2 : calculator
def calculator(state:MessagesState):
    user_query = state["messages"][-1].content.lower()
    if "add" in user_query:
        numbers = [int(s) for s in user_query.split() if s.isdigit()]
        result = sum(numbers)
        return {"messages":[f"The result of addition is {result}."]}
    
    return {"messages":["I can only perform addition now."]}

# node3 : default node
def default(state:MessagesState):
    return {"messages":["Sorry, I don't understand that request"]}

# node 4 : to decide which node should call 
def routing_function(state:MessagesState):
    last_message = state["messages"][-1].content.lower()
    if "weather" in last_message or "temperature" in last_message:
        return "weather"
    elif "add" in last_message or "calculate" in last_message:
        return "calculator"
    return "default"

# Workflow

workflow = StateGraph(MessagesState)

workflow.add_node("weather",weather)
workflow.add_node("calculator",calculator)
workflow.add_node("default",default)
workflow.add_node("routing_function",routing_function)

workflow.add_conditional_edges(START,routing_function) # here we start from routing function because user msg first go to that function and then decide which node should be call
workflow.add_edge("weather",END)
workflow.add_edge("calculator",END)
workflow.add_edge("default",END)

app = workflow.compile()

def interact_agent():

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit","quit"]:
            print("Conversation Terminated")
            break
        input_var = {"messages":[("human",user_input)]}

        for chunk in app.stream(input_var,stream_mode = "values"):
            chunk["messages"][-1].pretty_print()

interact_agent()


