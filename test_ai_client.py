#!/usr/bin/env python
"""
Test script to verify AI client functionality with priority system.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append('/home/mahamudh472/Project/backend_chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_chatbot.settings')
django.setup()

from chat.ai_client import ai_client

def test_ai_client():
    print("=== AI Client Test ===")
    print(f"Active Provider: {ai_client.get_active_provider()}")
    print("\nProvider Status:")
    status = ai_client.get_provider_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test embedding functionality
    print("\n=== Testing Embeddings ===")
    try:
        test_text = "This is a test document for embedding."
        embedding = ai_client.embed_text(test_text)
        print(f"✅ Embedding generated successfully")
        print(f"   Embedding dimensions: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"❌ Embedding test failed: {e}")
    
    # Test chat functionality
    print("\n=== Testing Chat ===")
    try:
        test_prompt = "What is the company's mission?"
        test_context = "Our company mission is to provide excellent customer service and innovative solutions."
        response = ai_client.chat_with_context(test_prompt, test_context)
        print(f"✅ Chat response generated successfully")
        print(f"   Response: {response[:100]}...")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")

if __name__ == "__main__":
    test_ai_client()
