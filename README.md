🛠️ Customer Support Ticket Resolution Agent

An AI-powered customer support automation system built using LangGraph, designed to streamline ticket handling, resolution, and escalation.
This project demonstrates the use of orchestration, prompt engineering, and agent-based architecture to create intelligent workflows for support operations.

📌 Features

✅ Ticket Classification – Categorizes support tickets (billing, technical, account, etc.)

✅ Contextual Resolution – Suggests responses using LLM-powered agents

✅ Escalation Handling – Routes unresolved queries to a higher-level support agent

✅ Knowledge Base Integration – Pulls solutions from stored knowledge/articles

✅ LangGraph Orchestration – Manages multi-step agent workflows efficiently

🧩 Tech Stack

LangGraph → Orchestration & agent-based architecture

LangChain → LLM interaction & tools

OpenAI API → LLM for response generation

Python → Core development


🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/Simran65/Support-Ticket-Resolution-Agent.git
cd Support-Ticket-Resolution-Agent

2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here

5️⃣ Run the Agent
python demo.py

📂 Project Structure
📦 Support-Ticket-Resolution-Agent
 ┣ 📜 main.py            # Entry point
 ┣ 📜 agent_graph.py     # LangGraph orchestration logic
 ┣ 📜 prompt_templates.py # Prompt engineering templates
 ┣ 📜 requirements.txt
 ┣ 📜 .env.example
 ┗ 📜 README.md
