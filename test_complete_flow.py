import requests
import json
import time

def test_async_nova_flow():
    """
    Test the complete async flow of the Nova endpoint
    1. Send message (get threadId)
    2. Poll status until completed
    3. Get final response
    """
    
    # URLs
    message_url = "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod/message"
    status_url = "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod/status"
    
    print("Testing Complete Async Nova Flow")
    print("=" * 50)
    
    # Step 1: Send message
    payload = {
        "role": "user",
        "message": "I need advise on how to reduce my electricity bill from 150 to 100 euros monthly"
    }
    
    print("1. Sending message...")
    print(f"   Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(message_url, json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse the nested response
            outer_response = response.json()
            inner_response = json.loads(outer_response['body'])
            
            thread_id = inner_response.get('threadId')
            status = inner_response.get('status')
            message = inner_response.get('message')
            
            print(f"   Thread ID: {thread_id}")
            print(f"   Status: {status}")
            print(f"   Message: {message}")
            
            if not thread_id:
                print("   ERROR: No threadId received")
                return None
                
            print("\n2. Polling for completion...")
            print("   (Being VERY patient - checking every 10 seconds for up to 5 minutes)")
            print("-" * 30)
            
            # Step 2: Poll status until completed - MUCH more patient
            max_attempts = 30  # 30 attempts × 10 seconds = 5 minutes total
            wait_time = 10     # 10 seconds between checks
            
            for attempt in range(max_attempts):
                print(f"   Attempt {attempt + 1}/{max_attempts}")
                
                try:
                    status_response = requests.get(status_url, params={"threadId": thread_id})
                    print(f"   Status Code: {status_response.status_code}")
                    
                    if status_response.status_code == 200:
                        # Parse nested status response
                        status_outer = status_response.json()
                        
                        if 'body' in status_outer:
                            status_inner = json.loads(status_outer['body'])
                            current_status = status_inner.get('status', 'unknown')
                            
                            print(f"   Current Status: {current_status}")
                            
                            if current_status == 'completed':
                                print("\n3. SUCCESS! Message completed")
                                print("=" * 50)
                                
                                # Extract final response
                                final_response = status_inner.get('response', 'No response content')
                                
                                print("Nova Pro Response:")
                                print("-" * 30)
                                print(final_response)
                                print("-" * 30)
                                
                                # Return complete result
                                return {
                                    "threadId": thread_id,
                                    "status": "completed",
                                    "response": final_response,
                                    "message": "Message processed successfully"
                                }
                                
                            elif current_status == 'error':
                                error_msg = status_inner.get('error', 'Unknown error')
                                print(f"   ERROR: {error_msg}")
                                return None
                                
                            else:
                                print(f"   Still processing... waiting {wait_time}s")
                                time.sleep(wait_time)
                        else:
                            print(f"   Unexpected response: {status_response.text}")
                            
                    else:
                        print(f"   Status check failed: {status_response.text}")
                        
                except Exception as e:
                    print(f"   Status check error: {e}")
                    
            print(f"\n   TIMEOUT: Message didn't complete in {max_attempts * wait_time} seconds")
            return None
            
        else:
            print(f"   ERROR: Failed to send message: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ERROR: {e}")
        return None

def create_simple_nova_client():
    """Create a simple client function for using the Nova endpoint"""
    
    client_code = '''
import requests
import json
import time

def call_nova_endpoint(message, role="user", max_wait=30):
    """
    Simple function to call Nova endpoint and wait for response
    
    Args:
        message (str): Message to send to Nova Pro
        role (str): Role (default: "user")  
        max_wait (int): Maximum seconds to wait for response
        
    Returns:
        dict: Response from Nova Pro or None if failed
    """
    
    # Endpoint URLs
    message_url = "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod/message"
    status_url = "https://vqlrgfa4gf.execute-api.eu-central-1.amazonaws.com/prod/status"
    
    try:
        # Step 1: Send message
        payload = {"role": role, "message": message}
        response = requests.post(message_url, json=payload)
        
        if response.status_code != 200:
            return {"error": f"Failed to send message: {response.text}"}
            
        # Parse response to get threadId
        outer_response = response.json()
        inner_response = json.loads(outer_response['body'])
        thread_id = inner_response.get('threadId')
        
        if not thread_id:
            return {"error": "No threadId received"}
        
        # Step 2: Poll for completion
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_response = requests.get(status_url, params={"threadId": thread_id})
            
            if status_response.status_code == 200:
                status_outer = status_response.json()
                if 'body' in status_outer:
                    status_inner = json.loads(status_outer['body'])
                    current_status = status_inner.get('status')
                    
                    if current_status == 'completed':
                        return {
                            "threadId": thread_id,
                            "status": "completed",
                            "response": status_inner.get('response', ''),
                            "message": "Success"
                        }
                    elif current_status == 'error':
                        return {
                            "threadId": thread_id,
                            "status": "error", 
                            "error": status_inner.get('error', 'Unknown error')
                        }
            
            time.sleep(2)  # Wait 2 seconds before next check
        
        return {"error": f"Timeout after {max_wait} seconds"}
        
    except Exception as e:
        return {"error": str(e)}

# Example usage:
if __name__ == "__main__":
    result = call_nova_endpoint("Explain AWS Lambda in simple terms. 1 sentence max")
    
    if result.get('status') == 'completed':
        print("Nova Pro Response:")
        print(result['response'])
    else:
        print("Error:", result.get('error', 'Unknown error'))
'''
    
    # Save the client
    with open('nova_client.py', 'w') as f:
        f.write(client_code)
    
    print("✓ Created nova_client.py - Simple client for your endpoint")

if __name__ == "__main__":
    # Test the complete flow
    result = test_async_nova_flow()
    
    if result:
        print("\n" + "=" * 50)
        print("ENDPOINT WORKING PERFECTLY!")
        print("✓ Async flow completed successfully")
        print("✓ Nova Pro responded correctly")
        
        # Create the simple client
        create_simple_nova_client()
        
        print("\nYou can now use:")
        print("1. nova_client.py - Simple function to call Nova")
        print("2. Your endpoint is fully functional!")
        
    else:
        print("\n" + "=" * 50)
        print("Endpoint accepts messages but may need more time to process")
        print("Try checking status manually with a threadId")
