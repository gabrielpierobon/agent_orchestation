#!/usr/bin/env python3
"""
AWS Bedrock Nova Pro Client
Wrapper for the async AWS API Gateway + Lambda + Bedrock endpoint
"""

import requests
import json
import time
from typing import Dict, Optional


class AWSBedrockNovaClient:
    def __init__(self, endpoint_base_url: str = None):
        """
        Initialize AWS Bedrock Nova Pro client
        
        Args:
            endpoint_base_url: Base URL for the API Gateway endpoint
                             Default: https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod
        """
        self.endpoint_base_url = endpoint_base_url or "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod"
        self.message_url = f"{self.endpoint_base_url}/message"
        self.status_url = f"{self.endpoint_base_url}/status"
        
        print(f"✅ AWS Bedrock Nova Pro client initialized")
        print(f"   Endpoint: {self.endpoint_base_url}")
    
    def send_message(self, message: str, role: str = "user", system_prompt: str = None) -> Dict:
        """
        Send a message to the Nova Pro endpoint (async)
        
        Args:
            message: The message content
            role: The role (default: "user")
            system_prompt: Optional system prompt (handled by Lambda)
            
        Returns:
            Dict with threadId and initial status
        """
        payload = {
            "role": role,
            "message": message
        }
        
        # If system_prompt is provided, include it (Lambda should handle it)
        if system_prompt:
            payload["system_prompt"] = system_prompt
        
        try:
            print(f"📞 Sending message to Nova Pro endpoint...")
            response = requests.post(self.message_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                # Parse nested response
                outer_response = response.json()
                inner_response = json.loads(outer_response['body'])
                
                thread_id = inner_response.get('threadId')
                status = inner_response.get('status', 'unknown')
                
                print(f"✅ Message sent successfully")
                print(f"   Thread ID: {thread_id}")
                print(f"   Status: {status}")
                
                return {
                    "threadId": thread_id,
                    "status": status,
                    "message": inner_response.get('message', 'Processing')
                }
            else:
                error_msg = f"Failed to send message: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return {"error": error_msg}
                
        except Exception as e:
            error_msg = f"Failed to send message: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}
    
    def get_status(self, thread_id: str) -> Dict:
        """
        Get the status of a message processing thread
        
        Args:
            thread_id: The thread ID from send_message
            
        Returns:
            Dict with current status and response (if completed)
        """
        try:
            response = requests.get(self.status_url, params={"threadId": thread_id}, timeout=10)
            
            if response.status_code == 200:
                # Parse nested response
                outer_response = response.json()
                
                if 'body' in outer_response:
                    inner_response = json.loads(outer_response['body'])
                    return inner_response
                else:
                    return {"error": "Unexpected response format"}
            else:
                return {"error": f"Status check failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Failed to get status: {str(e)}"}
    
    def wait_for_completion(self, thread_id: str, max_wait_time: int = 120, poll_interval: int = 5) -> Dict:
        """
        Wait for message processing to complete
        
        Args:
            thread_id: The thread ID from send_message
            max_wait_time: Maximum time to wait in seconds (default: 120)
            poll_interval: Seconds between status checks (default: 5)
            
        Returns:
            Dict with final response or error
        """
        start_time = time.time()
        attempts = 0
        
        print(f"⏳ Waiting for completion (max {max_wait_time}s, checking every {poll_interval}s)...")
        
        while time.time() - start_time < max_wait_time:
            attempts += 1
            status_result = self.get_status(thread_id)
            
            current_status = status_result.get('status', 'unknown')
            
            if current_status == 'completed':
                print(f"✅ Message completed after {attempts} attempts ({int(time.time() - start_time)}s)")
                return {
                    "status": "completed",
                    "response": status_result.get('response', ''),
                    "threadId": thread_id
                }
            elif current_status == 'error':
                error_msg = status_result.get('error', 'Unknown error')
                print(f"❌ Message failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "threadId": thread_id
                }
            else:
                print(f"   Attempt {attempts}: status={current_status}, waiting {poll_interval}s...")
                time.sleep(poll_interval)
        
        timeout_msg = f"Timeout after {max_wait_time}s"
        print(f"⚠️  {timeout_msg}")
        return {
            "status": "timeout",
            "error": timeout_msg,
            "threadId": thread_id
        }
    
    def send_and_wait(self, message: str, role: str = "user", system_prompt: str = None, 
                     max_wait_time: int = 120, poll_interval: int = 5) -> Dict:
        """
        Send a message and wait for the response (convenience method)
        
        Args:
            message: The message content
            role: The role (default: "user")
            system_prompt: Optional system prompt
            max_wait_time: Maximum time to wait in seconds (default: 120)
            poll_interval: Seconds between status checks (default: 5)
            
        Returns:
            Dict with final response or error
        """
        # Step 1: Send message
        send_result = self.send_message(message, role, system_prompt)
        
        if "error" in send_result:
            return send_result
        
        thread_id = send_result.get('threadId')
        
        if not thread_id:
            return {"error": "No threadId received"}
        
        # Step 2: Wait for completion
        return self.wait_for_completion(thread_id, max_wait_time, poll_interval)


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = AWSBedrockNovaClient()
    
    # Test message
    test_message = "What are the best ways to reduce electricity consumption in an apartment?"
    
    print("\n" + "="*60)
    print("Testing AWS Bedrock Nova Pro Client")
    print("="*60)
    
    # Send and wait for response
    result = client.send_and_wait(
        message=test_message,
        role="user",
        max_wait_time=120,
        poll_interval=5
    )
    
    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    
    if result.get('status') == 'completed':
        print("✅ SUCCESS!")
        print("\nNova Pro Response:")
        print("-" * 60)
        print(result['response'])
        print("-" * 60)
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")

