from src.WorkflowEngine.ticket_state import TicketState
import csv

def log_escalation(state):
    with open("escalation_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            state["ticket"]["subject"],
            state["ticket"]["description"],
            state["category"],
            state["draft"],
            state["review_feedback"]
        ])


def retry_or_escalate(state: TicketState) -> str:
    retry_count = state.get("retry_count", 0)
    
    # If we have a final response, we're done
    if state.get("final_response"):
        print(f"   🎯 WORKFLOW COMPLETE: Response approved after {retry_count} attempts")
        return "end"
    
    # If we've tried 2 times already, escalate
    if retry_count >= 2:
        print(f"   🚨 MAXIMUM RETRIES REACHED: Escalating to human review")
        print(f"   📋 Logging to escalation_log.csv")
        log_escalation(state)
        return "end"
    
    # Increment retry count and continue
    state["retry_count"] = retry_count + 1
    print(f"   🔄 RETRY #{state['retry_count']}: Refining context based on feedback")
    print(f"   💡 Feedback: {state.get('review_feedback', 'No feedback')[:80]}...")
    return "retrieve"
