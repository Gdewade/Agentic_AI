from langgraph.graph import StateGraph,START,END,MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]

# MessageState class means state already inbuilt in langgraph so we directly used that

def node1(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("node1",node1)
builder.add_edge(START,"node1")
builder.add_edge("node1",END)

app = builder.compile()

def interact_agent():
    while True:
        user_input = input("You : ")
        if user_input.lower() in ["exit","quit"]:
            print("Conversation Terminate")
            break
        input_variables = {
            "messages": [HumanMessage(content=user_input)]
        }

        # for continous conversation like chatbot we used 'stream'
        for chunk in app.stream(input_variables,stream_mode="values"):
            chunk["messages"][-1].pretty_print()

interact_agent()