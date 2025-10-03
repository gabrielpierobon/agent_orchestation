#!/usr/bin/env python3
"""
Test script for Multi-Agent Orchestrator with AWS Bedrock Nova Pro
"""

import requests
import json
import time

def test_orchestrator():
    """Test the multi-agent orchestrator with AWS Bedrock Nova Pro"""
    
    orchestrator_url = "http://localhost:8080/orchestrate-energy"
    health_url = "http://localhost:8080/health"
    
    print("="*60)
    print("Testing Multi-Agent Orchestrator with AWS Bedrock Nova Pro")
    print("="*60)
    
    # Step 1: Check health
    print("\n1. Checking orchestrator health...")
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Orchestrator is healthy!")
            print(f"   - Agents registered: {health_data.get('agents_registered', 0)}")
            print(f"   - AWS Bedrock ready: {health_data.get('aws_bedrock_ready', False)}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to orchestrator: {e}")
        print("\n💡 Make sure the orchestrator is running:")
        print("   python multi_agent_orchestrator_aws.py")
        return None
    
    # Step 2: Send energy consultation request
    print("\n2. Sending energy consultation request...")
    
    payload = {
        "task": "energy efficiency consultation",
        "data": {
            "customer_id": "CUST-2025-001",
            "inquiry": "I want to reduce my electricity bill from 150 to 100 euros monthly",
            "home_type": "apartment",
            "current_bill": 150
        }
    }
    
    print(f"   Request payload:")
    print(f"   {json.dumps(payload, indent=2)}")
    
    try:
        print("\n   Sending request... (this may take 2-3 minutes)")
        print("   📋 Step 1: n8n processes customer data")
        print("   📋 Step 2: SAP enriches with enterprise data")
        print("   📋 Step 3: AWS Bedrock Nova Pro provides recommendations ⏳")
        print("   📋 Step 4: Salesforce checks service history")
        print("   📋 Step 5: n8n validates recommendations")
        
        start_time = time.time()
        response = requests.post(orchestrator_url, json=payload, timeout=180)  # 3 min timeout
        elapsed_time = time.time() - start_time
        
        print(f"\n   Response received in {elapsed_time:.1f} seconds")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*60)
            print("✅ ORCHESTRATION COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            # Display workflow status
            print(f"\nWorkflow Status: {result.get('status', 'unknown').upper()}")
            print(f"Workflow Type: {result.get('workflow', 'unknown')}")
            
            # Display agents used
            print("\n🤖 Agents Used:")
            for agent in result.get('agents_used', []):
                print(f"   • {agent['agent']} ({agent['type']}) - {agent['role']}")
            
            # Display step results
            print("\n📊 Step Results:")
            
            print("\n   1️⃣  Customer Processing:")
            customer_data = result.get('step1_customer_processing', {})
            print(f"      {json.dumps(customer_data, indent=6)[:200]}...")
            
            print("\n   2️⃣  SAP Enterprise Enrichment:")
            sap_data = result.get('step2_sap_enrichment', {})
            account_status = sap_data.get('account_status', {})
            print(f"      Account: {account_status.get('account_number', 'N/A')}")
            print(f"      Status: {account_status.get('status', 'N/A')}")
            print(f"      Eligible Programs: {len(sap_data.get('eligibility_summary', {}).get('recommended_programs', []))}")
            
            print("\n   3️⃣  AWS Bedrock Nova Pro Recommendations:")
            ai_data = result.get('step3_ai_recommendations', {})
            if 'error' in ai_data:
                print(f"      ❌ Error: {ai_data['error']}")
            else:
                print(f"      Status: {ai_data.get('agent_status', 'unknown')}")
                recommendations = ai_data.get('recommendations', [])
                print(f"      Recommendations: {len(recommendations)} programs")
                response_preview = ai_data.get('consultation_response', '')[:150]
                print(f"      Preview: {response_preview}...")
            
            print("\n   4️⃣  Salesforce Service History:")
            sf_data = result.get('step4_salesforce_history', {})
            print(f"      Summary: {sf_data.get('summary', 'N/A')[:100]}...")
            
            print("\n   5️⃣  Validation Result:")
            validation_data = result.get('step5_validation', {})
            print(f"      {json.dumps(validation_data, indent=6)[:200]}...")
            
            # Display final summary
            print("\n📋 Consultation Summary:")
            summary = result.get('consultation_summary', {})
            print(f"   • Validation Passed: {summary.get('validation_passed', False)}")
            print(f"   • Estimated Savings: {summary.get('estimated_savings', 'N/A')}")
            print(f"   • Recommended Programs: {len(summary.get('recommended_programs', []))}")
            
            print("\n" + "="*60)
            print("🎉 AWS Bedrock Nova Pro Integration Working!")
            print("="*60)
            
            return result
            
        else:
            print(f"\n❌ Orchestration failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return None
            
    except requests.exceptions.Timeout:
        print("\n⚠️  Request timed out (> 3 minutes)")
        print("   This might be normal if Nova Pro is taking longer to respond")
        return None
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return None


if __name__ == "__main__":
    result = test_orchestrator()
    
    if result:
        print("\n✅ Test completed successfully!")
        print("   The orchestrator is working with AWS Bedrock Nova Pro")
    else:
        print("\n❌ Test failed or incomplete")
        print("   Check the orchestrator logs for more details")

