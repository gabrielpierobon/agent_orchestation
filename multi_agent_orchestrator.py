#!/usr/bin/env python3
"""
Multi-Agent Orchestrator - 3 Agent System
- 2 n8n agents (customer processing & validation)
- 1 Azure AI Foundry agent (energy customer service)

Usage: python multi_agent_orchestrator.py
Then: curl -X POST http://localhost:8080/orchestrate-energy -H "Content-Type: application/json" -d '{"task": "energy efficiency consultation", "data": {"customer_id": "12345", "inquiry": "I want to reduce my electricity bill", "home_type": "apartment", "current_bill": 150}}'
"""

from flask import Flask, request, jsonify
import requests
import json
from typing import Dict, List
import sys
import os

# Import our Azure AI Foundry client
from azure_ai_foundry_client import AzureAIFoundryClient

class MultiAgentRegistry:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent_id: str, agent_type: str, capabilities: List[str], config: Dict):
        """Register an agent with its type, capabilities and configuration"""
        self.agents[agent_id] = {
            "agent_type": agent_type,  # "n8n" or "azure_ai"
            "capabilities": capabilities,
            "config": config,
            "status": "active"
        }
        print(f"✓ Registered {agent_type} agent '{agent_id}' with capabilities: {capabilities}")
    
    def discover_by_capability(self, capability: str) -> List[Dict]:
        """Find agents that have the required capability"""
        matching_agents = []
        for agent_id, agent_info in self.agents.items():
            if capability in agent_info["capabilities"]:
                matching_agents.append({
                    "agent_id": agent_id,
                    "agent_type": agent_info["agent_type"],
                    "config": agent_info["config"]
                })
        return matching_agents
    
    def get_agent(self, agent_id: str) -> Dict:
        """Get specific agent by ID"""
        return self.agents.get(agent_id)

class MultiAgentOrchestrator:
    def __init__(self):
        self.app = Flask(__name__)
        self.registry = MultiAgentRegistry()
        self.azure_ai_client = None
        self.setup_routes()
    
    def initialize_azure_client(self):
        """Initialize Azure AI Foundry client"""
        try:
            self.azure_ai_client = AzureAIFoundryClient()
            print("✅ Azure AI Foundry client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Azure AI client: {str(e)}")
            return False
    
    def setup_routes(self):
        @self.app.route('/agents/register', methods=['POST'])
        def register_agent():
            """Register a new agent"""
            data = request.json
            self.registry.register_agent(
                agent_id=data['agent_id'],
                agent_type=data['agent_type'],
                capabilities=data['capabilities'], 
                config=data['config']
            )
            return jsonify({"status": "registered", "agent_id": data['agent_id']})
        
        @self.app.route('/agents/discover/<capability>', methods=['GET'])
        def discover_agents(capability):
            """Discover agents by capability"""
            agents = self.registry.discover_by_capability(capability)
            return jsonify({"capability": capability, "agents": agents})
        
        @self.app.route('/orchestrate-energy', methods=['POST'])
        def orchestrate_energy_consultation():
            """Main 3-agent orchestration endpoint for energy consultations"""
            task_data = request.json
            result = self.orchestrate_three_agent_energy_task(task_data)
            return jsonify(result)
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "agents_registered": len(self.registry.agents),
                "azure_ai_ready": self.azure_ai_client is not None
            })
    
    def orchestrate_three_agent_energy_task(self, task_data):
        """Orchestrate energy consultation task across 3 agents"""
        task = task_data.get('task', '')
        data = task_data.get('data', {})
        
        print(f"🎯 Three-agent energy consultation task: {task}")
        print(f"📊 Customer data: {data}")
        
        try:
            # STEP 1: Process customer data with n8n customer agent
            print("\n📋 STEP 1: Processing customer data with n8n agent...")
            customer_agents = self.registry.discover_by_capability("customer_processing")
            if not customer_agents:
                return {"error": "No customer processing agent available"}
            
            customer_result = self.call_n8n_agent(
                customer_agents[0]['config']['webhook_url'], 
                "process energy customer inquiry", 
                data
            )
            
            print(f"✅ Step 1 completed: {customer_result}")
            
            # STEP 2: Get energy recommendations from Azure AI agent
            print("\n📋 STEP 2: Getting energy efficiency recommendations from Azure AI agent...")
            azure_agents = self.registry.discover_by_capability("energy_consultation")
            if not azure_agents:
                return {"error": "No Azure AI energy consultation agent available"}
            
            # Prepare data for Azure AI agent
            energy_consultation_data = {
                "customer_profile": customer_result,
                "original_inquiry": data.get('inquiry', ''),
                "home_type": data.get('home_type', ''),
                "current_bill": data.get('current_bill', 0),
                "request_type": "energy_efficiency_consultation"
            }
            
            ai_recommendations = self.call_azure_ai_agent(
                azure_agents[0]['config']['agent_id'],
                energy_consultation_data
            )
            
            print(f"✅ Step 2 completed: AI recommendations received")
            
            # STEP 3: Validate recommendations with n8n validation agent
            print("\n📋 STEP 3: Validating recommendations with n8n validation agent...")
            validation_agents = self.registry.discover_by_capability("recommendation_validation")
            if not validation_agents:
                return {"error": "No validation agent available"}
            
            # Prepare validation data
            validation_data = {
                "customer_data": customer_result,
                "ai_recommendations": ai_recommendations,
                "validation_type": "energy_efficiency_compliance",
                "original_inquiry": data
            }
            
            validation_result = self.call_n8n_agent(
                validation_agents[0]['config']['webhook_url'],
                "validate energy efficiency recommendations",
                validation_data
            )
            
            print(f"✅ Step 3 completed: {validation_result}")
            
            return {
                "status": "completed",
                "task": task,
                "workflow": "three_agent_energy_consultation",
                "agents_used": [
                    {
                        "agent": customer_agents[0]['agent_id'], 
                        "type": "n8n",
                        "role": "customer_data_processor"
                    },
                    {
                        "agent": azure_agents[0]['agent_id'], 
                        "type": "azure_ai",
                        "role": "energy_consultant"
                    },
                    {
                        "agent": validation_agents[0]['agent_id'], 
                        "type": "n8n",
                        "role": "recommendation_validator"
                    }
                ],
                "step1_customer_processing": customer_result,
                "step2_ai_recommendations": ai_recommendations,
                "step3_validation": validation_result,
                "final_status": validation_result.get('approval_status', 'unknown'),
                "consultation_summary": {
                    "customer_profile": customer_result,
                    "recommended_programs": ai_recommendations.get('recommendations', []),
                    "validation_passed": validation_result.get('validation_passed', False),
                    "estimated_savings": validation_result.get('estimated_savings', 'N/A')
                }
            }
            
        except Exception as e:
            error_msg = f"Orchestration failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg, "status": "failed"}
    
    def call_n8n_agent(self, webhook_url: str, task: str, data: Dict) -> Dict:
        """Call n8n agent via webhook"""
        payload = {
            "task": task,
            "data": data,
            "timestamp": "2025-01-18T10:00:00Z",
            "source": "multi_agent_orchestrator"
        }
        
        try:
            print(f"📞 Calling n8n agent at: {webhook_url}")
            response = requests.post(
                webhook_url, 
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"🔍 n8n Response Status: {response.status_code}")
            
            if response.status_code == 200:
                if response.content:
                    result = response.json()
                    
                    # Handle n8n array response
                    if isinstance(result, list) and len(result) > 0:
                        extracted = result[0].get('output', result[0])
                        return extracted
                    else:
                        return result
                else:
                    return {"message": "Success - No content"}
            else:
                return {"error": f"n8n agent returned status {response.status_code}"}
                    
        except Exception as e:
            error_msg = f"Failed to call n8n agent: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def call_azure_ai_agent(self, agent_id: str, consultation_data: Dict) -> Dict:
        """Call Azure AI Foundry agent for energy consultation"""
        try:
            print(f"📞 Calling Azure AI agent: {agent_id}")
            
            if not self.azure_ai_client:
                raise Exception("Azure AI client not initialized")
            
            # Create a conversation thread
            thread = self.azure_ai_client.create_thread()
            thread_id = thread["id"]
            
            # Prepare the consultation message
            customer_profile = consultation_data.get('customer_profile', {})
            inquiry = consultation_data.get('original_inquiry', '')
            home_type = consultation_data.get('home_type', '')
            current_bill = consultation_data.get('current_bill', 0)
            
            consultation_message = f"""
I have a customer inquiry about energy efficiency. Here are the details:

Customer Profile: {json.dumps(customer_profile, indent=2)}
Original Inquiry: {inquiry}
Home Type: {home_type}
Current Monthly Bill: ${current_bill}

Please provide specific energy efficiency program recommendations that would help this customer reduce their electricity costs. Include:
1. Recommended programs with descriptions
2. Expected savings potential
3. Implementation timeline
4. Any eligibility requirements

Focus on practical, actionable recommendations.
"""
            
            # Send message to the agent
            self.azure_ai_client.send_message(thread_id, consultation_message)
            
            # Run the agent
            run = self.azure_ai_client.run_agent(thread_id, agent_id)
            run_id = run["id"]
            
            # Wait for completion
            completed_run = self.azure_ai_client.wait_for_run_completion(thread_id, run_id, max_wait_time=60)
            
            if completed_run["status"] == "completed":
                # Get the agent's response
                messages = self.azure_ai_client.get_messages(thread_id)
                
                # Extract the latest assistant message
                for message in messages.get("data", []):
                    if message.get("role") == "assistant":
                        content = message.get("content", [])
                        for content_item in content:
                            if content_item.get("type") == "text":
                                ai_response = content_item.get("text", {}).get("value", "")
                                return {
                                    "consultation_response": ai_response,
                                    "recommendations": self.parse_recommendations(ai_response),
                                    "thread_id": thread_id,
                                    "agent_status": "completed"
                                }
                
                return {"error": "No assistant response found"}
            else:
                return {"error": f"Azure AI agent run failed with status: {completed_run['status']}"}
                
        except Exception as e:
            error_msg = f"Failed to call Azure AI agent: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def parse_recommendations(self, ai_response: str) -> List[Dict]:
        """Parse AI response to extract structured recommendations"""
        # Simple parsing - in production, this would be more sophisticated
        recommendations = []
        
        # Look for numbered recommendations or bullet points
        lines = ai_response.split('\n')
        current_rec = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.')) or line.startswith('•'):
                if current_rec:
                    recommendations.append(current_rec)
                current_rec = {"title": line, "description": ""}
            elif current_rec and line:
                current_rec["description"] += line + " "
        
        if current_rec:
            recommendations.append(current_rec)
        
        return recommendations
    
    def run(self):
        print("🚀 Starting Multi-Agent Orchestrator (3 Agents)...")
        print("📋 Available endpoints:")
        print("  POST /agents/register - Register new agent")
        print("  GET  /agents/discover/<capability> - Find agents by capability") 
        print("  POST /orchestrate-energy - Execute 3-agent energy consultation")
        print("  GET  /health - Health check")
        
        print(f"\n🤖 Registered Agents: {len(self.registry.agents)}")
        for agent_id, agent_info in self.registry.agents.items():
            print(f"  • {agent_id} ({agent_info['agent_type']}) - {agent_info['capabilities']}")
        
        print("\n🎯 To execute a 3-agent energy consultation, run:")
        print('curl -X POST http://localhost:8080/orchestrate-energy -H "Content-Type: application/json" -d \'{"task": "energy efficiency consultation", "data": {"customer_id": "12345", "inquiry": "I want to reduce my electricity bill", "home_type": "apartment", "current_bill": 150}}\'')
        print("\n" + "="*80)
        
        self.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Initialize Azure AI client
    if not orchestrator.initialize_azure_client():
        print("❌ Cannot start without Azure AI client. Please check your configuration.")
        sys.exit(1)
    
    # Register n8n customer processing agent
    orchestrator.registry.register_agent(
        agent_id="n8n-customer-processor",
        agent_type="n8n",
        capabilities=["customer_processing", "data_analysis"],
        config={
            "webhook_url": "https://gabrielpierobon.app.n8n.cloud/webhook/931a4dbc-3fa5-432f-8c1c-a60206a46b4a"
        }
    )
    
    # Register Azure AI energy consultation agent
    orchestrator.registry.register_agent(
        agent_id="asst_aq7lhFm8W8ldxwte9pynGlsk",  # Your existing agent ID
        agent_type="azure_ai",
        capabilities=["energy_consultation", "customer_service", "energy_efficiency"],
        config={
            "agent_id": "asst_aq7lhFm8W8ldxwte9pynGlsk",
            "model": "gpt-4o",
            "instructions": "You are a helpful customer service agent for an energy company. Provide clear, accurate information about energy efficiency programs and services."
        }
    )
    
    # Register n8n validation agent
    orchestrator.registry.register_agent(
        agent_id="n8n-recommendation-validator",
        agent_type="n8n",
        capabilities=["recommendation_validation", "compliance_check", "risk_assessment"],
        config={
            "webhook_url": "https://gabrielpierobon.app.n8n.cloud/webhook/7c319881-0ba1-4cce-8c34-34d59b276569"
        }
    )
    
    print("🎉 All 3 agents registered successfully!")
    print("🔧 Agent Architecture:")
    print("  1️⃣  n8n Customer Processor → processes initial customer data")
    print("  2️⃣  Azure AI Energy Consultant → provides energy efficiency recommendations") 
    print("  3️⃣  n8n Recommendation Validator → validates and approves recommendations")
    print()
    
    # Start server
    orchestrator.run()
