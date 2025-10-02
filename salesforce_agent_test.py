#!/usr/bin/env python3
"""
Salesforce Agentforce Agent API Test Script
Tests communication with a Salesforce Agentforce agent
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SalesforceAgentClient:
    def __init__(self):
        self.consumer_key = os.getenv('SALESFORCE_CONSUMER_KEY')
        self.consumer_secret = os.getenv('SALESFORCE_CONSUMER_SECRET')
        self.agent_id = os.getenv('SALESFORCE_AGENT_ID')
        self.instance_url = os.getenv('SALESFORCE_INSTANCE_URL')
        self.access_token = None
        self.session_id = None
        
        # Validate configuration
        if not all([self.consumer_key, self.consumer_secret, self.agent_id, self.instance_url]):
            raise ValueError("Missing required Salesforce configuration in .env file")
    
    def authenticate(self):
        """Obtain OAuth2 access token using client credentials flow"""
        print("🔐 Authenticating with Salesforce...")
        
        token_url = f"{self.instance_url}/services/oauth2/token"
        
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret
        }
        
        try:
            response = requests.post(token_url, data=payload, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            
            # Update instance URL from token response (important for sandboxes)
            if 'instance_url' in token_data:
                self.instance_url = token_data['instance_url']
            
            print(f"✅ Authentication successful!")
            print(f"   Token type: {token_data.get('token_type', 'Bearer')}")
            print(f"   Instance URL: {self.instance_url}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            return False
    
    def check_api_versions(self):
        """Check available API versions and resources"""
        print(f"\n🔍 Checking available API versions...")
        
        versions_url = f"{self.instance_url}/services/data/"
        
        try:
            response = requests.get(versions_url, timeout=30)
            response.raise_for_status()
            
            versions = response.json()
            print(f"✅ Found {len(versions)} API versions")
            
            # Show latest versions
            latest = versions[-3:] if len(versions) >= 3 else versions
            for v in latest:
                print(f"   - {v['label']} ({v['version']})")
            
            # Try to check resources for latest version
            if versions:
                latest_version = versions[-1]['version']
                resources_url = f"{self.instance_url}/services/data/v{latest_version}/"
                
                print(f"\n🔍 Checking ALL resources for v{latest_version}...")
                response = requests.get(resources_url, headers={'Authorization': f'Bearer {self.access_token}'}, timeout=30)
                
                if response.status_code == 200:
                    resources = response.json()
                    print(f"✅ Total resources: {len(resources)}")
                    
                    # Search for Einstein/AI/Agent resources
                    einstein_keys = [k for k in resources.keys() if 'einstein' in k.lower() or 'agent' in k.lower() or 'ai' in k.lower()]
                    
                    if einstein_keys:
                        print(f"\n🎯 Einstein/AI/Agent resources found:")
                        for key in einstein_keys:
                            print(f"   ✅ {key}: {resources[key]}")
                    else:
                        print(f"\n⚠️  No Einstein/AI/Agent resources in standard API")
                        print(f"   Sample resources: {', '.join(list(resources.keys())[:10])}")
                    
                    # Explore the /ai resource
                    if 'ai' in [k.lower() for k in resources.keys()]:
                        print(f"\n🔍 Exploring /ai resource...")
                        headers = {'Authorization': f'Bearer {self.access_token}'}
                        ai_url = f"{self.instance_url}/services/data/v{latest_version}/ai"
                        
                        try:
                            ai_resp = requests.get(ai_url, headers=headers, timeout=10)
                            if ai_resp.status_code == 200:
                                ai_data = ai_resp.json()
                                print(f"   ✅ /ai resource contents:")
                                print(f"      {json.dumps(ai_data, indent=6)}")
                        except Exception as e:
                            print(f"   ⚠️  Error exploring /ai: {str(e)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to check API versions: {str(e)}")
            return False
    
    def start_session(self):
        """Start a new session with the Agentforce agent using OFFICIAL API endpoint"""
        print(f"\n🚀 Starting session with agent {self.agent_id}...")
        
        # OFFICIAL API endpoint (singular 'agent', not plural 'agents')
        session_url = f"https://api.salesforce.com/einstein/ai-agent/v1/agents/{self.agent_id}/sessions"
        
        # Generate a random UUID for session tracking
        import uuid
        session_key = str(uuid.uuid4())
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Payload according to official documentation
        payload = {
            'externalSessionKey': session_key,
            'instanceConfig': {
                'endpoint': self.instance_url
            },
            'streamingCapabilities': {
                'chunkTypes': ['Text']
            },
            'bypassUser': True
        }
        
        try:
            print(f"   Endpoint: {session_url}")
            print(f"   Session Key: {session_key}")
            response = requests.post(session_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            session_data = response.json()
            self.session_id = session_data['sessionId']
            
            print(f"✅ Session created successfully!")
            print(f"   Session ID: {self.session_id}")
            
            # Show initial greeting message if present
            if 'messages' in session_data and len(session_data['messages']) > 0:
                greeting = session_data['messages'][0].get('message', '')
                print(f"   Agent greeting: {greeting}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to start session: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            return False
    
    def send_message(self, message):
        """Send a message to the agent and get response"""
        print(f"\n💬 Sending message to agent...")
        print(f"   Message: \"{message}\"")
        
        # OFFICIAL API endpoint for sending messages
        message_url = f"https://api.salesforce.com/einstein/ai-agent/v1/sessions/{self.session_id}/messages/stream"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Message payload with correct structure including sequenceId
        payload = {
            'message': {
                'type': 'Text',
                'text': message,
                'sequenceId': 1
            }
        }
        
        try:
            # Stream the response (Server-Sent Events)
            response = requests.post(message_url, headers=headers, json=payload, stream=True, timeout=60)
            response.raise_for_status()
            
            print(f"\n✅ Agent is responding...")
            print(f"\n{'='*80}")
            print(f"🤖 AGENT RESPONSE:")
            print(f"{'='*80}\n")
            
            messages = []
            
            # Read the streaming response and collect all messages
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    
                    # SSE format: "data: {json}"
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove "data: " prefix
                        
                        try:
                            data = json.loads(data_str)
                            
                            # Try multiple possible structures
                            text_chunk = None
                            if 'message' in data:
                                # Try different message structures
                                if isinstance(data['message'], str):
                                    text_chunk = data['message']
                                elif 'text' in data['message']:
                                    text_chunk = data['message']['text']
                                elif 'message' in data['message']:
                                    text_chunk = data['message']['message']
                            elif 'text' in data:
                                text_chunk = data['text']
                            
                            if text_chunk:
                                messages.append(text_chunk)
                        except json.JSONDecodeError:
                            continue
            
            # The last (longest) message is usually the complete one
            final_message = max(messages, key=len) if messages else ""
            
            print(final_message)
            
            print(f"\n{'='*80}\n")
            
            return {'response': final_message} if final_message else None
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send message: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Failed to send message: {str(e)}")
            return None
    
    def end_session(self):
        """
        End the session with the agent.
        Note: Salesforce Agentforce sessions expire automatically, so explicit ending is optional.
        """
        if not self.session_id:
            return
        
        print(f"✅ Session {self.session_id} will expire automatically.\n")
        self.session_id = None

def main():
    print("="*80)
    print("🌟 SALESFORCE AGENTFORCE API TEST")
    print("="*80)
    
    client = SalesforceAgentClient()
    
    try:
        # Step 1: Authenticate
        if not client.authenticate():
            print("\n❌ Cannot proceed without authentication")
            return
        
        # Step 2: Check API availability (diagnostic)
        client.check_api_versions()
        
        # Step 3: Start session
        if not client.start_session():
            print("\n❌ Cannot proceed without session")
            return
        
        # Step 4: Send test message
        test_message = "I have a package that was not delivered on time. Give me 3 ideas to solve this problem."
        
        response = client.send_message(test_message)
        
        if response:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed - no response received")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    finally:
        # Step 5: Clean up - end session
        client.end_session()
        
    print("="*80)
    print("🏁 Test finished")
    print("="*80)

if __name__ == "__main__":
    main()

