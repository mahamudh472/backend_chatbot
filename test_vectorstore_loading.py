#!/usr/bin/env python
"""
Simple test script to verify that vectorstore loading works correctly.
This will test the /vectorstore/stats/ endpoint to trigger lazy loading.
"""

import requests
import json

def test_vectorstore_loading():
    url = "http://127.0.0.1:8000/vectorstore/stats/"
    
    try:
        # This should trigger the vectorstore loading
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Vectorstore loaded successfully!")
            print(f"Stats: {json.dumps(data, indent=2)}")
        elif response.status_code == 401:
            print("Authentication required - this is expected for a protected endpoint")
        elif response.status_code == 503:
            print("Vectorstore not available - there might be an issue")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000/")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_vectorstore_loading()
