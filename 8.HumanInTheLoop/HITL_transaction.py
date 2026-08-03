from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()

# state
class State(TypedDict):
    amount:float

# node

def define_transaction(state:State):
    print("Defining transaction ...")
    return state

def verify_transaction(state:State):
    print(f"Verifying transaction amount:{state['amount']}")
    return state

# workflow

workflow = StateGraph(State)

workflow.add_node("define_transaction",define_transaction)
workflow.add_node("verify_transaction",verify_transaction)

workflow.add_edge(START,"define_transaction")
workflow.add_edge("define_transaction","verify_transaction")
workflow.add_edge("verify_transaction",END)

app = workflow.compile(interrupt_before=["verify_transaction"],checkpointer=MemorySaver())

initial_input = {"amount":1000.0}
config = {"configurable":{"thread_id":"thread-1"}}

for event in app.stream(initial_input,config):
    print(event)

user_approval = input("Apporval this transaction ? (yes/no):")
if user_approval.lower() =="yes":
    for event in app.stream(None,config):
        print(event)
else:
    print("Transaction cancelled.")