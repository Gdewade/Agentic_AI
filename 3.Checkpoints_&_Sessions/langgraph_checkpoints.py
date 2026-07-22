from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini")

def node1(state:MessagesState):
    msg = state["messages"]
    response = llm.invoke(msg)
    return {"messages":[response]}

workflow = StateGraph(MessagesState)

workflow.add_node("node1",node1)

workflow.add_edge(START,"node1")
workflow.add_edge("node1",END)

checkpointer = MemorySaver()

app = workflow.compile(checkpointer=checkpointer)

def interact_agent():

    thread_id = "session1"

    while True:

        user_input = input("You: ")
        if user_input.lower() in ["exit","quit"]:
            print("Terminated")
            break

        input_var = {
            "messages":[("human",user_input)]
        }

        config = {
            "configurable":{"thread_id":thread_id}
        }

        for chunk in app.stream(input_var, stream_mode= "values", config=config):
            chunk["messages"][-1].pretty_print()

interact_agent()





