from typing import Dict 
import csv
import json
import os
from src.WorkflowEngine.nodes import construct_workflow
from src.WorkflowEngine.ticket_state import TicketState

# Set API key directly if .env file doesn't exist
if not os.path.exists('.env'):
    os.environ['GROQ_API_KEY'] = 'key'

graph = construct_workflow()

def run_agent(ticket: Dict[str, str]):
    initial_state = TicketState(
        ticket=ticket,
        category="",
        context=[],
        draft="",
        review_feedback="",
        retry_count=0,
        final_response=None
    )
    result = graph.invoke(initial_state, config={"thread_id": "ticket-001", "recursion_limit": 50})
    return result


if __name__ == "__main__":
   
    with open("escalation_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "Description", "Category", "Draft", "Feedback"])

    test_ticket = {
        "subject": "Payment gateway error",
        "description": "I'm trying to make a purchase but getting a 'transaction failed' error every time I enter my card details."
    }

    print("🚀 Starting Support Ticket Resolution Agent...")
    print(f"📝 Processing ticket: {test_ticket['subject']}")
    print("=" * 60)

    result = run_agent(test_ticket)
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print("=" * 60)
    
    if result["final_response"]:
        print("✅ SUCCESS: Response approved!")
        print(f"📤 Final Response: {result['final_response']}")
    else:
        print("❌ ESCALATED: Response failed after 2 retries")
        print("📋 Check escalation_log.csv for details")
    
    print(f"🔄 Retry attempts: {result.get('retry_count', 0)}")
    print(f"🏷️  Category: {result.get('category', 'Unknown')}")