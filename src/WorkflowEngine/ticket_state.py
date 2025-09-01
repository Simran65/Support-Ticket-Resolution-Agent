from typing import TypedDict, Dict, List, Optional


class TicketState(TypedDict):
    ticket: Dict[str, str]
    category: str
    context: List[str]
    draft: str
    review_feedback: str
    retry_count: int
    final_response: Optional[str]
