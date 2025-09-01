from src.WorkflowEngine.ticket_state  import TicketState
from src.WorkflowEngine.nodes_def import classify_ticket, retrieve_context, generate_draft, review_draft 
from src.WorkflowEngine import retry
from langgraph.graph import StateGraph, END

def construct_workflow():
    workflow = StateGraph(TicketState)

    workflow.add_node("input", input_node)
    workflow.add_node("classify", classify_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("draft", draft_node)
    workflow.add_node("review", review_node)

    workflow.set_entry_point("input")
    workflow.add_edge("input", "classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "draft")
    workflow.add_edge("draft", "review")
    workflow.add_conditional_edges("review", retry.retry_or_escalate, {"retrieve": "retrieve", "end": END})

    return workflow.compile()

def input_node(state: TicketState) -> TicketState:
    print("📥 INPUT NODE: Processing ticket...")
    print(f"   Subject: {state['ticket']['subject']}")
    print(f"   Description: {state['ticket']['description']}")
    return state

def classify_node(state: TicketState) -> TicketState:
    print("\n🏷️  CLASSIFICATION NODE: Analyzing ticket...")
    state["category"] = classify_ticket(state["ticket"])
    print(f"   ✅ Classified as: {state['category']}")
    return state

def retrieve_node(state: TicketState) -> TicketState:
    print(f"\n🔍 RETRIEVAL NODE: Fetching context for {state['category']}...")
    state["context"] = retrieve_context(state["category"], state["ticket"], state.get("review_feedback", ""))
    print(f"   📚 Retrieved {len(state['context'])} context items")
    if state.get("review_feedback"):
        print(f"   💡 Using feedback: {state['review_feedback'][:100]}...")
    return state

def draft_node(state: TicketState) -> TicketState:
    print(f"\n✍️  DRAFT NODE: Generating response (Attempt {state.get('retry_count', 0) + 1})...")
    state["draft"] = generate_draft(state["ticket"], state["context"])
    print(f"   📝 Draft generated:")
    print(f"   {'='*50}")
    print(f"   {state['draft']}")
    print(f"   {'='*50}")
    return state

def review_node(state: TicketState) -> TicketState:
    print(f"\n🔍 REVIEW NODE: Evaluating draft...")
    review = review_draft(state["draft"], state["ticket"])
    state["review_feedback"] = review["feedback"]

    if review["pass"]:
        state["final_response"] = state["draft"]
        print(f"   ✅ REVIEW PASSED: Response approved!")
    else:
        print(f"   ❌ REVIEW FAILED: {review['feedback']}")
        print(f"   🔄 Will retry with feedback...")

    return state
