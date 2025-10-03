#!/usr/bin/env python3
"""
ACP Proof of Concept - Multi Agent Registry with n8n Webhook Integration
Usage: python acp_poc.py
Then: curl -X POST http://localhost:8080/orchestrate -H "Content-Type: application/json" -d '{"task": "process customer data", "data": {"customer_id": "12345"}}'
"""

from flask import Flask, request, jsonify
import requests
import json
from typing import Dict, List

class ACPRegistry:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent_id: str, capabilities: List[str], webhook_url: str):
        """Register an agent with its capabilities and n8n webhook URL"""
        self.agents[agent_id] = {
            "capabilities": capabilities,
            "webhook_url": webhook_url,
            "status": "active"
        }
        print(f"✓ Registered agent '{agent_id}' with capabilities: {capabilities}")
    
    def discover_by_capability(self, capability: str) -> List[Dict]:
        """Find agents that have the required capability"""
        matching_agents = []
        for agent_id, agent_info in self.agents.items():
            if capability in agent_info["capabilities"]:
                matching_agents.append({
                    "agent_id": agent_id,
                    "webhook_url": agent_info["webhook_url"]
                })
        return matching_agents

class ACPServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.registry = ACPRegistry()
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/agents/register', methods=['POST'])
        def register_agent():
            """Register a new agent - ACP Standard Endpoint"""
            data = request.json
            self.registry.register_agent(
                agent_id=data['agent_id'],
                capabilities=data['capabilities'], 
                webhook_url=data['webhook_url']
            )
            return jsonify({"status": "registered", "agent_id": data['agent_id']})
        
        @self.app.route('/agents/discover/<capability>', methods=['GET'])
        def discover_agents(capability):
            """Discover agents by capability - ACP Standard Endpoint"""
            agents = self.registry.discover_by_capability(capability)
            return jsonify({"capability": capability, "agents": agents})
        
        @self.app.route('/orchestrate', methods=['POST'])
        def orchestrate_task():
            """Main orchestration endpoint - calls agents based on task requirements"""
            task_data = request.json
            task = task_data.get('task', '')
            data = task_data.get('data', {})
            
            print(f"🎯 Received task: {task}")
            
            # Simple capability mapping (in real system, this would be more sophisticated)
            capability_map = {
                "customer": "customer_processing",
                "data": "data_analysis", 
                "process": "data_processing",
                "invoice": "invoice_processing"
            }
            
            # Determine required capability from task description
            required_capability = None
            for keyword, capability in capability_map.items():
                if keyword.lower() in task.lower():
                    required_capability = capability
                    break
            
            if not required_capability:
                return jsonify({"error": "Could not determine required capability from task"}), 400
            
            # Discover capable agents
            capable_agents = self.registry.discover_by_capability(required_capability)
            
            if not capable_agents:
                return jsonify({"error": f"No agent found with capability: {required_capability}"}), 404
            
            # Call the first available agent (round-robin could be implemented here)
            agent = capable_agents[0]
            result = self.call_n8n_agent(agent['webhook_url'], task, data)
            
            return jsonify({
                "status": "completed",
                "task": task,
                "agent_used": agent['agent_id'],
                "capability": required_capability,
                "result": result
            })
        
        @self.app.route('/orchestrate-multi', methods=['POST'])
        def orchestrate_multi_agent():
            """Multi-agent orchestration endpoint"""
            task_data = request.json
            result = self.orchestrate_multi_agent_task(task_data)
            return jsonify(result)
    
    def orchestrate_multi_agent_task(self, task_data):
        """Orchestrate tasks that require multiple agents"""
        task = task_data.get('task', '')
        data = task_data.get('data', {})
        
        print(f"🎯 Multi-agent task: {task}")
        
        # Step 1: Process customer data
        print("📋 Step 1: Processing customer data...")
        customer_agents = self.registry.discover_by_capability("customer_processing")
        if not customer_agents:
            return {"error": "No customer processing agent available"}
        
        customer_result = self.call_n8n_agent(
            customer_agents[0]['webhook_url'], 
            "process customer data", 
            data
        )
        
        # Step 2: Validate the processed data
        print("📋 Step 2: Validating processed data...")
        validation_agents = self.registry.discover_by_capability("data_validation")
        if not validation_agents:
            return {"error": "No validation agent available"}
        
        # Pass the result from first agent to second agent
        validation_data = {
            "original_data": data,
            "processed_result": customer_result,
            "validation_type": "customer_data_compliance"
        }
        
        validation_result = self.call_n8n_agent(
            validation_agents[0]['webhook_url'],
            "validate processed customer data",
            validation_data
        )
        
        return {
            "status": "completed",
            "task": task,
            "workflow": "multi_agent_collaboration",
            "agents_used": [
                {"agent": customer_agents[0]['agent_id'], "role": "data_processor"},
                {"agent": validation_agents[0]['agent_id'], "role": "validator"}
            ],
            "step1_processing": customer_result,
            "step2_validation": validation_result,
            "final_approval": validation_result.get('result', {}).get('approval_status', 'unknown')
        }
    
    def call_n8n_agent(self, webhook_url: str, task: str, data: Dict) -> Dict:
        """Call n8n agent via webhook - Direct Agent Communication"""
        payload = {
            "task": task,
            "data": data,
            "timestamp": "2025-01-18T10:00:00Z"
        }
        
        try:
            print(f"📞 Calling n8n agent at: {webhook_url}")
            response = requests.post(
                webhook_url, 
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            # DEBUG: Print raw response
            print(f"🔍 Status Code: {response.status_code}")
            print(f"🔍 Response Headers: {response.headers}")
            print(f"🔍 Raw Response: {response.text}")
            
            if response.status_code == 200:
                if response.content:
                    result = response.json()
                    print(f"✅ Parsed JSON: {result}")
                    
                    # Handle n8n array response
                    if isinstance(result, list) and len(result) > 0:
                        extracted = result[0].get('output', result[0])
                        print(f"✅ Extracted: {extracted}")
                        return extracted
                    else:
                        return result
                else:
                    print("❌ No content in response")
                    return {"message": "Success - No content"}
                    
        except Exception as e:
            error_msg = f"Failed to call agent: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def run(self):
        print("🚀 Starting ACP Server...")
        print("📋 Available endpoints:")
        print("  POST /agents/register - Register new agent")
        print("  GET  /agents/discover/<capability> - Find agents by capability") 
        print("  POST /orchestrate - Execute task with agent orchestration")
        print("  POST /orchestrate-multi - Execute multi-agent orchestration")
        print("\n🔧 To register your n8n agent, run:")
        print('curl -X POST http://localhost:8080/agents/register -H "Content-Type: application/json" -d \'{"agent_id": "n8n-agent-1", "capabilities": ["customer_processing", "data_analysis"], "webhook_url": "https://your-n8n-instance.com/webhook/your-webhook-id"}\'')
        print("\n🎯 To execute a single-agent task, run:")
        print('curl -X POST http://localhost:8080/orchestrate -H "Content-Type: application/json" -d \'{"task": "process customer data", "data": {"customer_id": "12345"}}\'')
        print("\n🎯 To execute a multi-agent task, run:")
        print('curl -X POST http://localhost:8080/orchestrate-multi -H "Content-Type: application/json" -d \'{"task": "process and validate customer", "data": {"customer_id": "12345"}}\'')
        print("\n" + "="*60)
        
        self.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Initialize and start ACP server
    server = ACPServer()
    
    # Auto-register first n8n agent (from environment variable)
    n8n_customer_url = os.getenv("N8N_CUSTOMER_AGENT")
    if not n8n_customer_url:
        print("⚠️  Warning: N8N_CUSTOMER_AGENT environment variable not set")
        n8n_customer_url = "https://gabrielpierobon.app.n8n.cloud/webhook/931a4dbc-3fa5-432f-8c1c-a60206a46b4a"
    
    server.registry.register_agent(
        agent_id="n8n-customer-agent",
        capabilities=["customer_processing", "data_analysis"],
        webhook_url=n8n_customer_url
    )
    
    # Auto-register second n8n agent (from environment variable)
    n8n_validation_url = os.getenv("N8N_VALIDATION_AGENT")
    if not n8n_validation_url:
        print("⚠️  Warning: N8N_VALIDATION_AGENT environment variable not set")
        n8n_validation_url = "https://gabrielpierobon.app.n8n.cloud/webhook/7c319881-0ba1-4cce-8c34-34d59b276569"
    
    server.registry.register_agent(
        agent_id="n8n-validation-agent",
        capabilities=["data_validation", "compliance_check", "risk_assessment"],
        webhook_url=n8n_validation_url
    )
    
    # Start server
    server.run()