import requests
from langgraph.graph import StateGraph, START, END, MessagesState

# weather_api_key = "afa07c153067e0f87a2ccd45b4f60712"
weather_api_key = "227fa444e2e7bbbe984f34122a9d6232"


# node : to fetch live weather data
def weather(state:MessagesState):
    #[-1] - means last message or last string/word
    user_query = state["messages"][-1].content
    city = user_query.split("in")[-1].strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    # API call
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return {"messages":[f"The weather in {city} is {temperature} C with {description}"]}
    else:
        return {"messages":["Sorry, I couldn't fetch the weather information"]}

# workflow

workflow = StateGraph(MessagesState)

workflow.add_node("weather",weather)

workflow.add_edge(START,"weather")
workflow.add_edge("weather",END)

app = workflow.compile()


def interact_agent():

    input_message= {"messages":[("human","Tell me weather in Pune")]}
    
    for result in app.stream(input_message,stream_mode="values"):
        result["messages"][-1].pretty_print()

interact_agent()
