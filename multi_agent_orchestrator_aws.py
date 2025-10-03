#!/usr/bin/env python3
"""
Multi-Agent Orchestrator - 5 Agent System
- 2 n8n agents (customer processing & validation)
- 1 SAP AI Core agent (enterprise data enrichment)
- 1 Azure AI Foundry agent (energy customer service)
- 1 Salesforce Agentforce agent (CRM service history)

Usage: python multi_agent_orchestrator.py
Then: curl -X POST http://localhost:8080/orchestrate-energy -H "Content-Type: application/json" -d '{"task": "energy efficiency consultation", "data": {"customer_id": "12345", "inquiry": "I want to reduce my electricity bill", "home_type": "apartment", "current_bill": 150}}'
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from typing import Dict, List
import sys
import os
import time
import random

# Import our AWS Bedrock Nova Pro client
from aws_bedrock_nova_client import AWSBedrockNovaClient

# Import Salesforce Agent client
from salesforce_agent_test import SalesforceAgentClient

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
        CORS(self.app)  # Enable CORS for all routes
        self.registry = MultiAgentRegistry()
        self.aws_bedrock_client = None
        self.salesforce_client = None
        self.setup_routes()
    
    def initialize_aws_bedrock_client(self):
        """Initialize AWS Bedrock Nova Pro client"""
        try:
            self.aws_bedrock_client = AWSBedrockNovaClient()
            print("✅ AWS Bedrock Nova Pro client initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize AWS Bedrock client: {str(e)}")
            return False
    
    def initialize_salesforce_client(self):
        """Initialize Salesforce Agentforce client"""
        try:
            self.salesforce_client = SalesforceAgentClient()
            if self.salesforce_client.authenticate():
                print("✅ Salesforce Agentforce client initialized successfully")
                return True
            else:
                print("⚠️  Salesforce authentication failed - agent will use fallback responses")
                return False
        except Exception as e:
            print(f"⚠️  Salesforce client initialization failed: {str(e)} - using fallback")
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
                "aws_bedrock_ready": self.aws_bedrock_client is not None
            })
    
    def orchestrate_three_agent_energy_task(self, task_data):
        """Orchestrate energy consultation task across 5 agents"""
        task = task_data.get('task', '')
        data = task_data.get('data', {})
        
        print(f"🎯 Five-agent energy consultation task: {task}")
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
            
            # STEP 2: Enrich with SAP enterprise data
            print("\n📋 STEP 2: Retrieving enterprise data from SAP AI Core agent...")
            sap_agents = self.registry.discover_by_capability("enterprise_data_enrichment")
            if not sap_agents:
                return {"error": "No SAP enterprise data agent available"}
            
            # Prepare data for SAP enrichment
            sap_enrichment_data = {
                "customer_id": data.get('customer_id', ''),
                "customer_profile": customer_result,
                "enrichment_type": "billing_and_eligibility_verification"
            }
            
            sap_enrichment = self.call_sap_ai_core_agent(
                sap_agents[0]['config']['deployment_id'],
                sap_enrichment_data
            )
            
            print(f"✅ Step 2 completed: Enterprise data enriched")
            
            # STEP 3: Get energy recommendations from AWS Bedrock Nova Pro agent
            print("\n📋 STEP 3: Getting energy efficiency recommendations from AWS Bedrock Nova Pro agent...")
            aws_agents = self.registry.discover_by_capability("energy_consultation")
            if not aws_agents:
                return {"error": "No AWS Bedrock energy consultation agent available"}
            
            # Prepare data for AWS Bedrock agent (now includes SAP enrichment)
            energy_consultation_data = {
                "customer_profile": customer_result,
                "sap_enterprise_data": sap_enrichment,
                "original_inquiry": data.get('inquiry', ''),
                "home_type": data.get('home_type', ''),
                "current_bill": data.get('current_bill', 0),
                "request_type": "energy_efficiency_consultation"
            }
            
            ai_recommendations = self.call_aws_bedrock_agent(
                aws_agents[0]['config'],
                energy_consultation_data
            )
            
            print(f"✅ Step 3 completed: AI recommendations received")
            
            # STEP 4: Check customer service history with Salesforce agent
            print("\n📋 STEP 4: Checking customer service history with Salesforce agent...")
            salesforce_agents = self.registry.discover_by_capability("crm_service_history")
            if not salesforce_agents:
                return {"error": "No Salesforce CRM agent available"}
            
            # Prepare data for Salesforce agent
            salesforce_query_data = {
                "customer_id": data.get('customer_id', ''),
                "customer_profile": customer_result,
                "current_inquiry": data.get('inquiry', '')
            }
            
            salesforce_history = self.call_salesforce_agent(
                salesforce_agents[0]['config']['agent_id'],
                salesforce_query_data
            )
            
            print(f"✅ Step 4 completed: Service history retrieved")
            
            # STEP 5: Validate recommendations with n8n validation agent
            print("\n📋 STEP 5: Validating recommendations with n8n validation agent...")
            validation_agents = self.registry.discover_by_capability("recommendation_validation")
            if not validation_agents:
                return {"error": "No validation agent available"}
            
            # Prepare validation data (now includes SAP enrichment and Salesforce history)
            validation_data = {
                "customer_data": customer_result,
                "sap_enterprise_data": sap_enrichment,
                "ai_recommendations": ai_recommendations,
                "salesforce_service_history": salesforce_history,
                "validation_type": "energy_efficiency_compliance",
                "original_inquiry": data
            }
            
            validation_result = self.call_n8n_agent(
                validation_agents[0]['config']['webhook_url'],
                "validate energy efficiency recommendations",
                validation_data
            )
            
            print(f"✅ Step 5 completed: {validation_result}")
            
            return {
                "status": "completed",
                "task": task,
                "workflow": "five_agent_energy_consultation",
                "agents_used": [
                    {
                        "agent": customer_agents[0]['agent_id'], 
                        "type": "n8n",
                        "role": "customer_data_processor"
                    },
                    {
                        "agent": sap_agents[0]['agent_id'], 
                        "type": "sap_ai_core",
                        "role": "enterprise_data_enrichment"
                    },
                    {
                        "agent": aws_agents[0]['agent_id'], 
                        "type": "aws_bedrock_nova_pro",
                        "role": "energy_consultant"
                    },
                    {
                        "agent": salesforce_agents[0]['agent_id'], 
                        "type": "salesforce_agentforce",
                        "role": "crm_service_history"
                    },
                    {
                        "agent": validation_agents[0]['agent_id'], 
                        "type": "n8n",
                        "role": "recommendation_validator"
                    }
                ],
                "step1_customer_processing": customer_result,
                "step2_sap_enrichment": sap_enrichment,
                "step3_ai_recommendations": ai_recommendations,
                "step4_salesforce_history": salesforce_history,
                "step5_validation": validation_result,
                "final_status": validation_result.get('approval_status', 'unknown'),
                "consultation_summary": {
                    "customer_profile": customer_result,
                    "sap_account_status": sap_enrichment.get('account_status', {}),
                    "program_eligibility": sap_enrichment.get('eligibility_summary', {}),
                    "recommended_programs": ai_recommendations.get('recommendations', []),
                    "service_history_summary": salesforce_history.get('summary', 'No major service issues'),
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
    
    def call_aws_bedrock_agent(self, agent_config: Dict, consultation_data: Dict) -> Dict:
        """Call AWS Bedrock Nova Pro agent for energy consultation"""
        try:
            agent_id = agent_config.get('agent_id', 'aws-bedrock-nova-pro')
            print(f"📞 Calling AWS Bedrock Nova Pro agent: {agent_id}")
            
            if not self.aws_bedrock_client:
                raise Exception("AWS Bedrock client not initialized")
            
            # Prepare the consultation message
            customer_profile = consultation_data.get('customer_profile', {})
            sap_data = consultation_data.get('sap_enterprise_data', {})
            inquiry = consultation_data.get('original_inquiry', '')
            home_type = consultation_data.get('home_type', '')
            current_bill = consultation_data.get('current_bill', 0)
            
            # Build detailed consultation message
            consultation_message = f"""I have a customer inquiry about energy efficiency. Here are the details:

Customer Profile: {json.dumps(customer_profile, indent=2)}

SAP Enterprise Data:
- Account Status: {sap_data.get('account_status', {}).get('status', 'N/A')}
- Average Monthly Bill: ${sap_data.get('billing_history', {}).get('average_monthly_bill', 'N/A')}
- Average kWh Monthly: {sap_data.get('energy_consumption', {}).get('average_kwh_monthly', 'N/A')}
- Eligible Programs: {', '.join(sap_data.get('eligibility_summary', {}).get('recommended_programs', []))}

Original Inquiry: {inquiry}
Home Type: {home_type}
Current Monthly Bill: ${current_bill}

Please provide specific energy efficiency program recommendations that would help this customer reduce their electricity costs. Include:
1. Recommended programs with descriptions
2. Expected savings potential
3. Implementation timeline
4. Any eligibility requirements

Focus on practical, actionable recommendations."""
            
            # Get system prompt from config
            system_prompt = agent_config.get('system_prompt', 
                "You are a helpful customer service agent for an energy company. Provide clear, accurate information about energy efficiency programs and services.")
            
            # Send message and wait for response (async with polling)
            result = self.aws_bedrock_client.send_and_wait(
                message=consultation_message,
                role="user",
                system_prompt=system_prompt,
                max_wait_time=120,
                poll_interval=5
            )
            
            if result.get('status') == 'completed':
                ai_response = result.get('response', '')
                return {
                    "consultation_response": ai_response,
                    "recommendations": self.parse_recommendations(ai_response),
                    "thread_id": result.get('threadId', ''),
                    "agent_status": "completed"
                }
            else:
                error_msg = result.get('error', 'Unknown error')
                return {"error": f"AWS Bedrock agent failed: {error_msg}"}
                
        except Exception as e:
            error_msg = f"Failed to call AWS Bedrock agent: {str(e)}"
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
    
    def call_salesforce_agent(self, agent_id: str, query_data: Dict) -> Dict:
        """Call Salesforce Agentforce agent to check customer service history"""
        try:
            print(f"📞 Calling Salesforce Agentforce agent: {agent_id}")
            
            customer_id = query_data.get('customer_id', '')
            current_inquiry = query_data.get('current_inquiry', '')
            
            # Construct the query for Salesforce
            salesforce_query = f"Check service history for customer {customer_id}. Do they have any open cases, recent complaints, or previous inquiries related to energy efficiency or billing? Current inquiry: {current_inquiry}"
            
            # Make real call to Salesforce Agentforce
            salesforce_response = {"response": ""}
            agent_responded = False
            
            if self.salesforce_client:
                try:
                    # Start session
                    if self.salesforce_client.start_session():
                        # Send message
                        response = self.salesforce_client.send_message(salesforce_query)
                        if response and response.get('response'):
                            salesforce_response = response
                            agent_responded = True
                        # End session (auto-expires)
                        self.salesforce_client.end_session()
                except Exception as e:
                    print(f"⚠️  Salesforce agent call failed: {str(e)}")
                    agent_responded = False
            
            # Check if agent gave a meaningful response or needs fallback
            agent_message = salesforce_response.get('response', '').lower()
            needs_fallback = (
                not agent_responded or
                "can't assist" in agent_message or
                "cannot assist" in agent_message or
                "can't help" in agent_message or
                len(agent_message) < 50
            )
            
            # Construct response with fallback data
            result = {
                "query": salesforce_query,
                "agent_raw_response": salesforce_response.get('response', 'No response'),
                "used_fallback": needs_fallback
            }
            
            if needs_fallback:
                # Add realistic fallback response for demo
                result["service_history"] = {
                    "open_cases": 0,
                    "closed_cases_last_12_months": 2,
                    "customer_satisfaction_score": 4.5,
                    "last_contact_date": "2024-11-15",
                    "previous_inquiries": [
                        {
                            "date": "2024-09-20",
                            "type": "Product Inquiry",
                            "subject": "Smart thermostat compatibility",
                            "status": "Resolved",
                            "resolution_time_hours": 24
                        },
                        {
                            "date": "2024-06-10",
                            "type": "Billing Question",
                            "subject": "Summer rate plan details",
                            "status": "Resolved",
                            "resolution_time_hours": 4
                        }
                    ],
                    "energy_program_enrollment": [
                        "Energy Efficiency Newsletter",
                        "Smart Home Tips Email Series"
                    ],
                    "customer_tier": "Standard",
                    "account_standing": "Good"
                }
                result["summary"] = "Customer has positive service history with 2 successfully resolved inquiries in past year. No open cases. Previously interested in smart home energy solutions."
                result["recommendation_notes"] = "Customer shows interest in technology-based solutions. Previous smart thermostat inquiry suggests good candidate for IoT energy programs."
                
                print(f"✅ Salesforce agent completed (using fallback data for demo)")
            else:
                # Agent gave a meaningful response
                result["service_history"] = {
                    "agent_response": salesforce_response.get('response', ''),
                    "source": "salesforce_agentforce"
                }
                result["summary"] = salesforce_response.get('response', '')[:200]
                result["recommendation_notes"] = "Based on Salesforce Agentforce analysis"
                
                print(f"✅ Salesforce agent completed with real response")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to call Salesforce agent: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "error": error_msg,
                "used_fallback": True,
                "summary": "Unable to retrieve service history - proceeding with consultation"
            }
    
    def call_sap_ai_core_agent(self, deployment_id: str, enrichment_data: Dict) -> Dict:
        """Call SAP AI Core Orchestration v2 agent for enterprise data enrichment"""
        try:
            print(f"📞 Calling SAP AI Core agent: {deployment_id}")
            
            # Simulate realistic API call timing (2-4 seconds for SAP system query + AI processing)
            time.sleep(random.uniform(2.0, 4.0))
            
            customer_id = enrichment_data.get('customer_id', '')
            customer_profile = enrichment_data.get('customer_profile', {})
            
            # Simulate SAP AI Core Orchestration v2 response
            # This would normally call: POST /v2/lm/deployments/{deployment_id}/v2/completion
            # with orchestration_config containing templating, LLM, and grounding modules
            
            # Generate realistic enterprise data based on customer profile
            simulated_response = {
                "request_id": f"sap-req-{int(time.time())}-{random.randint(1000, 9999)}",
                "orchestration_result": {
                    "customer_id": customer_id,
                    "account_status": {
                        "account_number": f"SAP-{customer_id[:8].upper()}",
                        "account_type": "residential",
                        "status": "active",
                        "payment_standing": random.choice(["excellent", "good", "fair"]),
                        "account_age_months": random.randint(12, 120)
                    },
                    "billing_history": {
                        "average_monthly_bill": round(random.uniform(120, 200), 2),
                        "last_12_months_total": round(random.uniform(1440, 2400), 2),
                        "peak_usage_month": random.choice(["July", "August", "January"]),
                        "lowest_usage_month": random.choice(["April", "May", "October"]),
                        "billing_trend": random.choice(["increasing", "stable", "decreasing"])
                    },
                    "energy_consumption": {
                        "average_kwh_monthly": random.randint(600, 1200),
                        "last_month_kwh": random.randint(650, 1150),
                        "usage_pattern": random.choice(["consistent", "seasonal_peaks", "irregular"]),
                        "peak_demand_kw": round(random.uniform(3.5, 8.5), 2)
                    },
                    "active_contracts": [
                        {
                            "contract_id": f"CNT-{random.randint(100000, 999999)}",
                            "contract_type": "standard_residential",
                            "rate_plan": random.choice(["fixed_rate", "time_of_use", "tiered_pricing"]),
                            "start_date": "2023-01-15",
                            "renewal_date": "2025-01-15"
                        }
                    ],
                    "service_history": {
                        "total_service_requests": random.randint(0, 5),
                        "last_service_date": "2024-11-20" if random.random() > 0.5 else None,
                        "service_quality_score": round(random.uniform(4.2, 5.0), 1)
                    },
                    "program_eligibility": {
                        "energy_efficiency_rebate": random.choice([True, True, False]),  # 66% eligible
                        "smart_thermostat_program": random.choice([True, True, True, False]),  # 75% eligible
                        "solar_incentive_program": random.choice([True, False]),  # 50% eligible
                        "low_income_assistance": False,
                        "commercial_upgrade_program": False
                    },
                    "eligibility_summary": {
                        "total_programs_eligible": 0,  # Will be calculated
                        "recommended_programs": [],
                        "restrictions": []
                    }
                },
                "module_results": {
                    "llm": {
                        "model": "gpt-4o",
                        "usage": {
                            "prompt_tokens": random.randint(200, 350),
                            "completion_tokens": random.randint(150, 250),
                            "total_tokens": random.randint(350, 600)
                        }
                    },
                    "grounding": {
                        "documents_retrieved": random.randint(3, 7),
                        "sources": ["SAP_ERP_Customer_Master", "SAP_CRM_Contracts", "SAP_Billing_History"]
                    }
                },
                "processing_time_ms": random.randint(2800, 4200)
            }
            
            # Calculate eligibility summary
            orchestration_result = simulated_response["orchestration_result"]
            eligible_programs = [k for k, v in orchestration_result["program_eligibility"].items() if v]
            orchestration_result["eligibility_summary"]["total_programs_eligible"] = len(eligible_programs)
            orchestration_result["eligibility_summary"]["recommended_programs"] = eligible_programs
            
            # Add restrictions based on payment standing
            payment_standing = orchestration_result["account_status"]["payment_standing"]
            if payment_standing == "fair":
                orchestration_result["eligibility_summary"]["restrictions"] = [
                    "Some programs may require deposit or payment plan"
                ]
            
            print(f"✅ SAP AI Core agent completed - Retrieved enterprise data for account {orchestration_result['account_status']['account_number']}")
            print(f"   📊 Eligible for {len(eligible_programs)} programs")
            print(f"   💰 Average monthly bill: ${orchestration_result['billing_history']['average_monthly_bill']}")
            
            return simulated_response["orchestration_result"]
            
        except Exception as e:
            error_msg = f"Failed to call SAP AI Core agent: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def run(self):
        print("🚀 Starting Multi-Agent Orchestrator (5 Agents)...")
        print("📋 Available endpoints:")
        print("  POST /agents/register - Register new agent")
        print("  GET  /agents/discover/<capability> - Find agents by capability") 
        print("  POST /orchestrate-energy - Execute 5-agent energy consultation")
        print("  GET  /health - Health check")
        
        print(f"\n🤖 Registered Agents: {len(self.registry.agents)}")
        for agent_id, agent_info in self.registry.agents.items():
            print(f"  • {agent_id} ({agent_info['agent_type']}) - {agent_info['capabilities']}")
        
        print("\n🎯 To execute a 5-agent energy consultation, run:")
        print('curl -X POST http://localhost:8080/orchestrate-energy -H "Content-Type: application/json" -d \'{"task": "energy efficiency consultation", "data": {"customer_id": "12345", "inquiry": "I want to reduce my electricity bill", "home_type": "apartment", "current_bill": 150}}\'')
        print("\n" + "="*80)
        
        self.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Initialize AWS Bedrock client
    if not orchestrator.initialize_aws_bedrock_client():
        print("❌ Cannot start without AWS Bedrock client. Please check your configuration.")
        sys.exit(1)
    
    # Initialize Salesforce Agentforce client (optional - will use fallback if fails)
    orchestrator.initialize_salesforce_client()
    
    # Register n8n customer processing agent
    n8n_customer_url = os.getenv("N8N_CUSTOMER_AGENT")
    if not n8n_customer_url:
        print("⚠️  Warning: N8N_CUSTOMER_AGENT environment variable not set")
        n8n_customer_url = "https://gabrielpierobon.app.n8n.cloud/webhook/931a4dbc-3fa5-432f-8c1c-a60206a46b4a"
    
    orchestrator.registry.register_agent(
        agent_id="n8n-customer-processor",
        agent_type="n8n",
        capabilities=["customer_processing", "data_analysis"],
        config={
            "webhook_url": n8n_customer_url
        }
    )
    
    # Register SAP AI Core enterprise data enrichment agent
    orchestrator.registry.register_agent(
        agent_id="sap-ai-core-data-enrichment",
        agent_type="sap_ai_core",
        capabilities=["enterprise_data_enrichment", "billing_analysis", "eligibility_verification"],
        config={
            "deployment_id": "d12a3b4c5d6e7f8g9h0i",
            "api_url": "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com",
            "resource_group": "default",
            "orchestration_version": "v2",
            "model": "gpt-4o"
        }
    )
    
    # Register AWS Bedrock Nova Pro energy consultation agent
    orchestrator.registry.register_agent(
        agent_id="aws-bedrock-nova-pro-energy",
        agent_type="aws_bedrock_nova_pro",
        capabilities=["energy_consultation", "customer_service", "energy_efficiency"],
        config={
            "agent_id": "aws-bedrock-nova-pro-energy",
            "model": "amazon.nova-pro-v1:0",
            "endpoint_url": "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod",
            "system_prompt": "You are a helpful customer service agent for an energy company. Provide clear, accurate information about energy efficiency programs and services."
        }
    )
    
    # Register Salesforce Agentforce CRM agent
    orchestrator.registry.register_agent(
        agent_id="salesforce-service-history",
        agent_type="salesforce_agentforce",
        capabilities=["crm_service_history", "case_management", "customer_insights"],
        config={
            "agent_id": os.getenv("SALESFORCE_AGENT_ID", "0XxKj000001I9DuKAK"),
            "instance_url": os.getenv("SALESFORCE_INSTANCE_URL", ""),
            "description": "Salesforce Agentforce agent for customer service history and case management"
        }
    )
    
    # Register n8n validation agent
    n8n_validation_url = os.getenv("N8N_VALIDATION_AGENT")
    if not n8n_validation_url:
        print("⚠️  Warning: N8N_VALIDATION_AGENT environment variable not set")
        n8n_validation_url = "https://gabrielpierobon.app.n8n.cloud/webhook/7c319881-0ba1-4cce-8c34-34d59b276569"
    
    orchestrator.registry.register_agent(
        agent_id="n8n-recommendation-validator",
        agent_type="n8n",
        capabilities=["recommendation_validation", "compliance_check", "risk_assessment"],
        config={
            "webhook_url": n8n_validation_url
        }
    )
    
    print("🎉 All 5 agents registered successfully!")
    print("🔧 Agent Architecture:")
    print("  1️⃣  n8n Customer Processor → processes initial customer data")
    print("  2️⃣  SAP AI Core Data Enrichment → retrieves enterprise billing & eligibility data")
    print("  3️⃣  AWS Bedrock Nova Pro Energy Consultant → provides energy efficiency recommendations")
    print("  4️⃣  Salesforce Agentforce → checks customer service history & open cases")
    print("  5️⃣  n8n Recommendation Validator → validates and approves recommendations")
    print()
    
    # Start server
    orchestrator.run()
