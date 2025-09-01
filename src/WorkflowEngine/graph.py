#!/usr/bin/env python3
"""
LangGraph compatible graph definition for the support ticket resolution system
"""

import os
from src.WorkflowEngine.nodes import construct_workflow

# Set API key directly if .env file doesn't exist
if not os.path.exists('.env'):
    os.environ['GROQ_API_KEY'] = 'key'

# Create the graph instance for langgraph dev
graph = construct_workflow()
