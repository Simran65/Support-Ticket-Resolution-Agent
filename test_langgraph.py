#!/usr/bin/env python3
"""
Test script to verify langgraph setup works
"""

import os
import json
import requests
import time

# Set API key
if not os.path.exists('.env'):
    os.environ['GROQ_API_KEY'] = 'api'

def test_langgraph_server():
    """Test the langgraph dev server"""
    
    # Wait a moment for server to start
    print("⏳ Waiting for langgraph server to start...")
    time.sleep(3)
    
    try:
        # Test ticket
        test_ticket = {
            "ticket": {
                "subject": "Payment gateway error",
                "description": "I'm trying to make a purchase but getting a 'transaction failed' error every time I enter my card details."
            },
            "category": "",
            "context": [],
            "draft": "",
            "review_feedback": "",
            "retry_count": 0,
            "final_response": None
        }
        
        # Test the langgraph API endpoint
        url = "http://localhost:8123/runs/stream"
        
        payload = {
            "assistant_id": "support_agent",
            "input": test_ticket,
            "stream_mode": ["values"]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        print("🚀 Testing langgraph dev server...")
        print(f"📡 Sending request to: {url}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✅ SUCCESS: Langgraph server is working!")
            print("📤 Response received")
            
            # Parse the response
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        if 'final_response' in data and data['final_response']:
                            print("🎯 Final Response:")
                            print(data['final_response'])
                            break
                    except json.JSONDecodeError:
                        continue
            
        else:
            print(f"❌ ERROR: Server responded with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to langgraph server")
        print("💡 Make sure 'langgraph dev' is running")
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_direct_graph():
    """Test the graph directly without server"""
    print("\n🔧 Testing direct graph execution...")
    
    try:
        from src.WorkflowEngine.nodes import construct_workflow
        from src.WorkflowEngine.ticket_state import TicketState
        
        graph = construct_workflow()
        
        initial_state = TicketState(
            ticket={
                "subject": "Payment gateway error",
                "description": "I'm trying to make a purchase but getting a 'transaction failed' error."
            },
            category="",
            context=[],
            draft="",
            review_feedback="",
            retry_count=0,
            final_response=None
        )
        
        result = graph.invoke(initial_state, config={"thread_id": "test-001", "recursion_limit": 50})
        
        print("✅ SUCCESS: Direct graph execution works!")
        print(f"🏷️ Category: {result.get('category', 'Unknown')}")
        print(f"🔄 Retries: {result.get('retry_count', 0)}")
        
        if result.get('final_response'):
            print("📤 Response generated successfully")
        else:
            print("⚠️ Ticket was escalated")
            
    except Exception as e:
        print(f"❌ ERROR in direct execution: {str(e)}")

if __name__ == "__main__":
    print("🧪 LANGGRAPH SETUP TEST")
    print("=" * 50)
    
    # Test direct execution first
    test_direct_graph()
    
    # Test langgraph server
    test_langgraph_server()
    
    print("\n✅ Test completed!")
