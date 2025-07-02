#!/usr/bin/env python3
"""
Test script for Meaning Agent
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.meaning_agent import MeaningAgent

def test_meaning_agent():
    """Test the Meaning Agent"""
    print("🧪 Testing Meaning Agent...")
    
    # Initialize agent
    agent = MeaningAgent()
    print(f"✅ Agent initialized: {agent.get_status()}")
    
    # Test cases
    test_cases = [
        {
            "name": "Simple LP Problem",
            "input": "Maximize profit: 3x + 4y subject to x + y <= 10, x >= 0, y >= 0",
            "objective": "maximize"
        },
        {
            "name": "LP Problem with Auxiliary Variables", 
            "input": "Maximize profit: 3x + 4y subject to x + y <= 10, x >= 0, y >= 0. Total production is x + y and resource usage is x + 2y.",
            "objective": "maximize"
        },
        {
            "name": "Minimization Problem",
            "input": "Minimize cost: 5x + 3y subject to x + 2y >= 8, x >= 0, y >= 0",
            "objective": "minimize"
        },
        {
            "name": "Invalid Problem",
            "input": "Hello, how are you?",
            "objective": "maximize"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print(f"Input: {test_case['input']}")
        
        # Process with agent
        result = agent.process_problem(test_case['input'], test_case['objective'])
        
        if result['success']:
            print("✅ Agent processing successful!")
            problem_data = result['result']
            
            print(f"📊 Problem type: {problem_data.get('problem_type', 'Unknown')}")
            print(f"🎯 Objective: {problem_data.get('objective', 'Unknown')}")
            print(f"📈 Confidence: {problem_data.get('confidence', 0.0)}")
            print(f"✅ Valid problem: {problem_data.get('is_valid_problem', False)}")
            
            # Check decision variables
            decision_vars = problem_data.get('decision_variables', {})
            print(f"🔢 Decision variables: {len(decision_vars)}")
            for var_name, var_info in decision_vars.items():
                print(f"   • {var_name}: {var_info.get('description', 'No description')}")
            
            # Check auxiliary variables
            auxiliary_vars = problem_data.get('auxiliary_variables', {})
            print(f"🔧 Auxiliary variables: {len(auxiliary_vars)}")
            for var_name, var_info in auxiliary_vars.items():
                equation = var_info.get('equation', 'No equation')
                print(f"   • {var_name}: {var_info.get('description', 'No description')} = {equation}")
            
            if problem_data.get('clarification'):
                print(f"❓ Clarification needed: {problem_data['clarification']}")
            
            # Validate output
            is_valid, error = agent.validate_output(problem_data)
            if is_valid:
                print("✅ Output validation PASSED!")
            else:
                print(f"❌ Output validation FAILED: {error}")
                
        else:
            print(f"❌ Agent processing failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Meaning Agent testing completed!")

def test_chat_context():
    """Test chat context functionality"""
    print("\n🧪 Testing Chat Context Functionality...")
    
    # Initialize agent
    agent = MeaningAgent()
    print("✅ Agent initialized for context testing")
    
    # Test building problem step by step
    print("\n📋 Test: Building problem step by step")
    
    # Step 1: Initial problem description
    print("Step 1: Initial description")
    result1 = agent.process_problem("I want to maximize profit from producing two products")
    
    if result1['success']:
        problem_data1 = result1['result']
        print(f"✅ Step 1: {problem_data1.get('problem_type', 'Unknown')} problem identified")
        print(f"   Decision variables: {list(problem_data1.get('decision_variables', {}).keys())}")
    else:
        print(f"❌ Step 1 failed: {result1.get('error', 'Unknown error')}")
    
    # Step 2: Add variables
    print("\nStep 2: Adding variables")
    result2 = agent.process_problem("The variables are x and y, representing quantities of products A and B")
    
    if result2['success']:
        problem_data2 = result2['result']
        print(f"✅ Step 2: Variables added")
        print(f"   Decision variables: {list(problem_data2.get('decision_variables', {}).keys())}")
    else:
        print(f"❌ Step 2 failed: {result2.get('error', 'Unknown error')}")
    
    # Step 3: Add objective
    print("\nStep 3: Adding objective")
    result3 = agent.process_problem("The objective is to maximize 3x + 4y")
    
    if result3['success']:
        problem_data3 = result3['result']
        print(f"✅ Step 3: Objective added")
        print(f"   Objective: {problem_data3.get('objective', 'Unknown')}")
    else:
        print(f"❌ Step 3 failed: {result3.get('error', 'Unknown error')}")
    
    # Step 4: Add constraints
    print("\nStep 4: Adding constraints")
    result4 = agent.process_problem("The constraints are x + y <= 10 and x >= 0, y >= 0")
    
    if result4['success']:
        problem_data4 = result4['result']
        print(f"✅ Step 4: Constraints added")
        print(f"   Constraints: {len(problem_data4.get('constraints', []))}")
        print(f"   Final problem valid: {problem_data4.get('is_valid_problem', False)}")
    else:
        print(f"❌ Step 4 failed: {result4.get('error', 'Unknown error')}")
    
    # Test chat history
    print(f"\n📝 Chat history length: {len(agent.chat_history)}")
    print("Chat history:")
    for i, msg in enumerate(agent.chat_history, 1):
        role = "User" if msg["sender"] == "user" else "Assistant"
        print(f"  {i}. {role}: {msg['message'][:50]}...")
    
    print("\n🎉 Chat Context testing completed!")

def test_casual_messages():
    """Test casual message handling"""
    print("\n🧪 Testing Casual Message Handling...")
    
    # Initialize agent
    agent = MeaningAgent()
    print("✅ Agent initialized for casual message testing")
    
    # Test casual greetings
    casual_messages = [
        "Oi",
        "Hello",
        "Hi there",
        "Bom dia",
        "Como vai?",
        "Tudo bem?"
    ]
    
    for message in casual_messages:
        print(f"\nTesting: '{message}'")
        result = agent.process_problem(message)
        
        if result['success']:
            problem_data = result['result']
            print(f"✅ Response: {problem_data.get('clarification', 'No clarification')[:50]}...")
            print(f"   Valid problem: {problem_data.get('is_valid_problem', False)}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Casual Message testing completed!")

def test_financial_consistency():
    """Test financial consistency validation"""
    print("\n🧪 Testing Financial Consistency Validation...")
    
    # Initialize agent
    agent = MeaningAgent()
    print("✅ Agent initialized for financial consistency testing")
    
    # Test problem with potential unit inconsistency
    test_problem = "Minimize cost: 1000*x + 1500*y subject to x + y <= 25, x >= 0, y >= 0"
    
    print(f"Testing problem: {test_problem}")
    result = agent.process_problem(test_problem)
    
    if result['success']:
        problem_data = result['result']
        print(f"✅ Problem processed successfully")
        print(f"   Problem type: {problem_data.get('problem_type', 'Unknown')}")
        print(f"   Confidence: {problem_data.get('confidence', 0.0)}")
        print(f"   Clarification: {problem_data.get('clarification', 'None')}")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Financial Consistency testing completed!")

if __name__ == "__main__":
    test_meaning_agent()
    test_chat_context()
    test_casual_messages()
    test_financial_consistency() 