from langgraph.graph import StateGraph, START, END
from typing import TypedDict


# ---------------- State ----------------

# Stores data shared between all nodes.
class ReActAgent(TypedDict):
    message: str
    action: str
    sub_action: str


# ---------------- Nodes ----------------

# Returns weather information.
def weather(state: ReActAgent):
    return {"message": "The weather is sunny today."}


# Returns latest news.
def news(state: ReActAgent):
    return {"message": "Here are the latest news headlines."}


# Returns recommendation based on sub_action.
def recommendation(state: ReActAgent):
    if state.get("sub_action") == "book":
        return {"message": "I recommend reading 'The Pragmatic Programmer'."}
    else:
        return {"message": "I have no other recommendation at the moment."}


# Decides which action to perform from the user's query.
def reasoning_node(state: ReActAgent):

    query = state["message"].lower()

    if "weather" in query:
        return {"action": "weather"}

    elif "news" in query:
        return {"action": "news"}

    elif "recommend" in query or "book" in query:
        return {
            "action": "recommendation",
            "sub_action": "book"
        }

    else:
        return {"action": "unknown"}


# Executes the correct subgraph based on the selected action.
def reasoning_parent(state: ReActAgent):

    if state["action"] == "weather":
        return weather_app.invoke(state)

    elif state["action"] == "news":
        return news_app.invoke(state)

    elif state["action"] == "recommendation":
        return recommendation_app.invoke(state)

    else:
        return {"message": "Sorry, I don't understand your request."}


# ---------------- Sub Graph Workflows ----------------

# Workflow for handling weather queries.
weather_workflow = StateGraph(ReActAgent)
weather_workflow.add_node("weather", weather)
weather_workflow.set_entry_point("weather")
weather_app = weather_workflow.compile()


# Workflow for handling news queries.
news_workflow = StateGraph(ReActAgent)
news_workflow.add_node("news", news)
news_workflow.set_entry_point("news")
news_app = news_workflow.compile()


# Workflow for handling recommendation queries.
recommendation_workflow = StateGraph(ReActAgent)
recommendation_workflow.add_node("recommendation", recommendation)
recommendation_workflow.set_entry_point("recommendation")
recommendation_app = recommendation_workflow.compile()


# ---------------- Parent Workflow ----------------

# Main workflow that connects reasoning with subgraphs.
reasoning_parent_workflow = StateGraph(ReActAgent)

reasoning_parent_workflow.add_node("reasoning_node", reasoning_node)
reasoning_parent_workflow.add_node("reasoning_parent", reasoning_parent)

reasoning_parent_workflow.add_edge(START, "reasoning_node")
reasoning_parent_workflow.add_edge("reasoning_node", "reasoning_parent")
reasoning_parent_workflow.add_edge("reasoning_parent", END)

react_agent_graph = reasoning_parent_workflow.compile()


# ---------------- Inputs ----------------

# Test weather query.
input_weather = {"message": "What is the weather today?"}
result_weather = react_agent_graph.invoke(input_weather)
print(result_weather["message"])


# Test news query.
input_news = {"message": "What is the latest news?"}
result_news = react_agent_graph.invoke(input_news)
print(result_news["message"])


# Test recommendation query.
input_recommendation = {"message": "Can you recommend a good book?"}
result_recommendation = react_agent_graph.invoke(input_recommendation)
print(result_recommendation["message"])