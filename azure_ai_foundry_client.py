import requests
import json
import os
import time
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AzureAIFoundryClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_AI_FOUNDRY_PROJECT_ENDPOINT")
        if not self.endpoint:
            raise ValueError("AZURE_AI_FOUNDRY_PROJECT_ENDPOINT environment variable is required")
        
        # For Azure AI Foundry Agent Service, use the GA API version
        self.api_version = "2025-05-01"  # GA API version for Agent Service
        
        # Debug output
        print(f"Endpoint: {self.endpoint}")
        print("Using DefaultAzureCredential authentication (Microsoft Entra ID)")
        
        # Azure AI Foundry Agent Service requires Microsoft Entra ID
        self.credential = DefaultAzureCredential()
        self.token = self._get_access_token()
    
    def _get_access_token(self):
        """Get Azure AD token for authentication"""
        try:
            # Use the correct scope for Azure AI Foundry (based on error message)
            token = self.credential.get_token("https://ai.azure.com/.default")
            return token.token
        except Exception as e:
            raise Exception(f"Failed to get Azure AD token: {str(e)}")
    
    def _get_headers(self):
        """Get authentication headers"""
        if not self.token:
            self.token = self._get_access_token()
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        
        print("Using Microsoft Entra ID Bearer token authentication")
        return headers
    
    def _make_request(self, method, url, headers=None, json_data=None):
        """Make HTTP request with error handling"""
        try:
            if headers is None:
                headers = self._get_headers()
            
            # Debug: Print the request details
            print(f"Making {method} request to: {url}")
            if json_data:
                print(f"Request payload: {json.dumps(json_data, indent=2)}")
            
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json_data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            raise
    
    def create_agent(self, name, instructions, model_deployment_name):
        """Create a new AI agent using the Agent Service API"""
        # Use the correct endpoint - Agent Service uses /assistants endpoint, not /agents
        url = f"{self.endpoint}/assistants?api-version={self.api_version}"
        
        payload = {
            "model": model_deployment_name,
            "name": name,
            "instructions": instructions,
            "tools": [{"type": "code_interpreter"}]
        }
        
        print(f"Creating agent: {name}")
        return self._make_request("POST", url, json_data=payload)
    
    def create_thread(self):
        """Create a conversation thread"""
        url = f"{self.endpoint}/threads?api-version={self.api_version}"
        
        print("Creating conversation thread...")
        return self._make_request("POST", url, json_data={})
    
    def send_message(self, thread_id, message_content):
        """Send message to agent"""
        url = f"{self.endpoint}/threads/{thread_id}/messages?api-version={self.api_version}"
        
        payload = {
            "role": "user",
            "content": message_content
        }
        
        print(f"Sending message: {message_content[:50]}...")
        return self._make_request("POST", url, json_data=payload)
    
    def run_agent(self, thread_id, agent_id):
        """Execute agent on thread"""
        url = f"{self.endpoint}/threads/{thread_id}/runs?api-version={self.api_version}"
        
        payload = {
            "assistant_id": agent_id  # Agent Service still uses assistant_id parameter
        }
        
        print("Running agent...")
        return self._make_request("POST", url, json_data=payload)
    
    def get_run_status(self, thread_id, run_id):
        """Get the status of a run"""
        url = f"{self.endpoint}/threads/{thread_id}/runs/{run_id}?api-version={self.api_version}"
        
        return self._make_request("GET", url)
    
    def wait_for_run_completion(self, thread_id, run_id, max_wait_time=60):
        """Wait for a run to complete"""
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            run_status = self.get_run_status(thread_id, run_id)
            status = run_status.get("status")
            print(f"Run status: {status}")
            
            if status in ["completed", "failed", "cancelled", "expired"]:
                return run_status
            
            time.sleep(2)
        
        raise TimeoutError(f"Run did not complete within {max_wait_time} seconds")
    
    def get_messages(self, thread_id):
        """Get thread messages"""
        url = f"{self.endpoint}/threads/{thread_id}/messages?api-version={self.api_version}"
        
        return self._make_request("GET", url)
    
    def get_agent(self, agent_id):
        """Get an existing agent by ID"""
        url = f"{self.endpoint}/assistants/{agent_id}?api-version={self.api_version}"
        
        print(f"Retrieving existing agent: {agent_id}")
        return self._make_request("GET", url)

# Usage Example
def main(agent_id=None):
    """
    Main function to interact with Azure AI Foundry Agent Service.
    
    Args:
        agent_id (str, optional): ID of existing agent to use. 
                                 If None, creates a new agent.
                                 
    Example:
        # Use existing agent
        main(agent_id="asst_aq7lhFm8W8ldxwte9pynGlsk")
        
        # Create new agent
        main()
    """
    try:
        # Initialize client
        client = AzureAIFoundryClient()
        
        # Use existing agent or create new one
        if agent_id:
            print("Step 1: Using existing AI agent...")
            agent = client.get_agent(agent_id)
            print(f"Retrieved agent: {agent.get('name', 'Unknown')} (ID: {agent_id})")
        else:
            print("Step 1: Creating AI agent...")
            agent = client.create_agent(
                name="Customer Service Agent",
                instructions="You are a helpful customer service agent for an energy company. Provide clear, accurate information about energy efficiency programs and services.",
                model_deployment_name="gpt-4o"  # Make sure this matches your deployment name
            )
            agent_id = agent["id"]
            print(f"Agent created with ID: {agent_id}")
        
        # Create conversation thread
        print("\nStep 2: Creating conversation thread...")
        thread = client.create_thread()
        thread_id = thread["id"]
        print(f"Thread created with ID: {thread_id}")
        
        # Send message
        print("\nStep 3: Sending message to agent...")
        message_content = "What are your energy efficiency programs and how can they help me save money on my electricity bill?"
        client.send_message(thread_id, message_content)
        
        # Run agent
        print("\nStep 4: Running agent...")
        run = client.run_agent(thread_id, agent_id)
        run_id = run["id"]
        print(f"Run started with ID: {run_id}")
        
        # Wait for completion
        print("\nStep 5: Waiting for agent response...")
        completed_run = client.wait_for_run_completion(thread_id, run_id)
        
        if completed_run["status"] == "completed":
            # Get response
            print("\nStep 6: Getting agent response...")
            messages = client.get_messages(thread_id)
            
            print("\n" + "="*50)
            print("CONVERSATION MESSAGES:")
            print("="*50)
            
            # Display messages in chronological order
            for message in reversed(messages.get("data", [])):
                role = message.get("role", "unknown")
                content = message.get("content", [])
                
                print(f"\n{role.upper()}:")
                for content_item in content:
                    if content_item.get("type") == "text":
                        print(content_item.get("text", {}).get("value", ""))
        else:
            print(f"Run failed with status: {completed_run['status']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nSetup Instructions:")
        print("1. Make sure to set the AZURE_AI_FOUNDRY_PROJECT_ENDPOINT environment variable in your .env file")
        print("   Example: AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project-name")
        print("\n2. Authentication requirements:")
        print("   - Azure AI Foundry Agent Service requires Microsoft Entra ID authentication")
        print("   - Install and login with Azure CLI: 'az login'")
        print("   - OR set environment variables for service principal authentication:")
        print("     AZURE_CLIENT_ID=your-client-id")
        print("     AZURE_CLIENT_SECRET=your-client-secret") 
        print("     AZURE_TENANT_ID=your-tenant-id")
        print("\n3. Install missing packages: pip install -r requirements.txt")
        print("\n4. Make sure you have proper permissions:")
        print("   - Azure AI Developer role or higher on the AI Foundry resource")

if __name__ == "__main__":
    # Use your existing agent ID here
    existing_agent_id = "asst_aq7lhFm8W8ldxwte9pynGlsk"  # Customer Service Agent
    main(agent_id=existing_agent_id)