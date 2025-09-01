from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Use the provided API key directly if .env is not available
api_key = os.getenv("GROQ_API_KEY", "key")

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Using the current llama3.1-8b model
    groq_api_key=api_key,
    temperature=0.1
)
