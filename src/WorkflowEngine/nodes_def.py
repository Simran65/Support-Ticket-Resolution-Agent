from typing import Dict ,List
import json
from langchain.schema import SystemMessage, HumanMessage
from src.core.llm import llm
from src.core.prompts import classify_prompt
from src.core.vector_store import vector_store
from src.core.prompts import draft_prompt
from src.core.prompts import review_prompt

def classify_ticket(ticket: Dict[str, str]) -> str:

    try:
        prompt = classify_prompt.format(
            subject=ticket["subject"],
            description=ticket["description"]
        )

        response = llm.invoke(
            [
                SystemMessage(content="You are a ticket classification assistant. Respond with a JSON object containing a 'category'."),
                HumanMessage(content=prompt)
            ],
            response_format={"type": "json_object"}
        )

        data = json.loads(response.content)
        category = data.get("category", "General")

        return category if category in {"Billing", "Technical", "Security", "General"} else "General"

    except Exception as e:
        print(f"Classification error: {e}")
        return "General"


def retrieve_context(category: str, ticket: dict, feedback: str = "") -> List[str]:
    try:
        query = f"{ticket['subject']} {ticket['description']}"
        if feedback:
            query += f" {feedback}"

        docs = vector_store.similarity_search(query=query, k=2, filter={"category": category})
        return [doc.page_content for doc in docs] or ["No relevant context found."]
    except Exception as e:
        print(f"Retrieval error: {str(e)}")
        return ["Retrieval failed."]


    
def generate_draft(ticket: dict, context: List[str]) -> str:
    try:
        context_str = "\n".join(context) if context else "No context available."
        prompt = draft_prompt.format(subject=ticket["subject"], description=ticket["description"], context=context_str)

        response = llm.invoke([
            SystemMessage(content="You are a customer support assistant. Generate a professional response as a plain text string."),
            HumanMessage(content=prompt)
        ])

        return response.content.strip()
    except Exception as e:
        print(f"Draft error: {str(e)}")
        return "Failed to generate draft."
    


def review_draft(draft: str, ticket: dict) -> Dict[str, str]:
    try:
        prompt = review_prompt.format(subject=ticket["subject"], description=ticket["description"], draft=draft)

        response = llm.invoke([
            SystemMessage(content="You are a quality assurance specialist. Review the draft response for accuracy, clarity, and policy compliance. Respond only with a JSON object containing 'pass' (boolean) and 'feedback' (string)."),
            HumanMessage(content=prompt)
        ], response_format={"type": "json_object"})

        data = json.loads(response.content)

        if "pass" in data and "feedback" in data:
            return data
        else:
            raise ValueError("Missing keys in response JSON.")
    except Exception as e:
        print(f"Review error: {str(e)}")
        return {"pass": False, "feedback": f"Review failed: {str(e)}. Please escalate to human review."}
