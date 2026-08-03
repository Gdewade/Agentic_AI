from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph,START,END,MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
load_dotenv()

# tool
@tool
def search(query:str):
    """Simulates a web search call."""
    return [f"The current weather in {query} is sunny and 75 F."]

# create toolnode of above tool
tool_node = ToolNode([search])

llm_obj = ChatOpenAI(model="gpt-4o-mini")
model = llm_obj.bind_tools([search])


# Define conditional logic to determine whether to continue or not
def should_continue(state:MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end" # no tools to call
    else:
        return "continue" # tool is there, continue to next step


# Define the function that simulates reasoning and invokes the model
# means here user response will be go and if tool is not there they ask to llm
def agent_reasoning(state:MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages":[response]}

# workflow

workflow = StateGraph(MessagesState)

workflow.add_node("agent_reasoning",agent_reasoning)
workflow.add_node("tool_node",tool_node)

workflow.add_edge(START,"agent_reasoning")
workflow.add_conditional_edges("agent_reasoning",should_continue,{
    "continue":"tool_node", # if there is tool then it will continue
    "end":END # if tool absent then workflow end
})

# memory
memory = MemorySaver()
app=workflow.compile(checkpointer=memory,interrupt_before=["tool_node"])

# initial input
initial_input = {"messages":[{"role":"user","content":"whats weather in san francisco ?"}]}
thread = {"configurable":{"thread_id":"1"}}

for event in app.stream(initial_input,thread,stream_mode="values"):
    print(event)

user_approval = input("Do you approve invoking the web search tool ? (yes/no):")

if user_approval.lower() == "yes":
    for event in app.stream(None,thread,stream_mode="values"):
        print(event)
else:
    print("Execution halted by user.")



