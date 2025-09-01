#!/usr/bin/env python3
"""
Demo Script for AI-Powered Support Ticket Resolution System

This script demonstrates different test scenarios and shows how the system
handles various types of support tickets.
"""

import json
import os
from src.main import run_agent

# Set API key directly if .env file doesn't exist
if not os.path.exists('.env'):
    os.environ['GROQ_API_KEY'] = 'key'

def demo_scenario_1():
    """Scenario 1: Billing Issue - Should succeed on first attempt"""
    print("🎭 SCENARIO 1: Billing Issue")
    print("=" * 60)
    
    ticket = {
        "subject": "Payment gateway error",
        "description": "I'm trying to make a purchase but getting a 'transaction failed' error every time I enter my card details."
    }
    
    result = run_agent(ticket)
    return result

def demo_scenario_2():
    """Scenario 2: Technical Issue - May require retry"""
    print("\n🎭 SCENARIO 2: Technical Issue")
    print("=" * 60)
    
    ticket = {
        "subject": "App crashes on startup",
        "description": "Every time I open the mobile app, it immediately crashes and closes. I've tried reinstalling but the problem persists."
    }
    
    result = run_agent(ticket)
    return result

def demo_scenario_3():
    """Scenario 3: Security Issue - Should be handled carefully"""
    print("\n🎭 SCENARIO 3: Security Issue")
    print("=" * 60)
    
    ticket = {
        "subject": "Suspicious login activity",
        "description": "I received an email about a login from an unknown location. I'm concerned my account might be compromised."
    }
    
    result = run_agent(ticket)
    return result

def demo_scenario_4():
    """Scenario 4: General Inquiry - Simple question"""
    print("\n🎭 SCENARIO 4: General Inquiry")
    print("=" * 60)
    
    ticket = {
        "subject": "How to update profile",
        "description": "I want to change my profile picture and update my contact information. Where can I do this?"
    }
    
    result = run_agent(ticket)
    return result

def main():
    """Run all demo scenarios"""
    print("🚀 AI-POWERED SUPPORT TICKET RESOLUTION SYSTEM - DEMO")
    print("=" * 80)
    print("This demo will show how the system handles different types of support tickets.")
    print("Each scenario demonstrates different aspects of the AI workflow.\n")
    
    # Run all scenarios
    results = []
    
    try:
        results.append(demo_scenario_1())
        results.append(demo_scenario_2())
        results.append(demo_scenario_3())
        results.append(demo_scenario_4())
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
        return
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        return
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 DEMO SUMMARY")
    print("=" * 80)
    
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result.get("final_response") else "❌ ESCALATED"
        category = result.get("category", "Unknown")
        retries = result.get("retry_count", 0)
        
        print(f"Scenario {i}: {status} | Category: {category} | Retries: {retries}")
    
    print("\n🎉 Demo completed! Check escalation_log.csv for any escalated tickets.")
    print("💡 Try modifying the test tickets in demo.py to test different scenarios.")

if __name__ == "__main__":
    main()
