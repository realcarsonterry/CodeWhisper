#!/usr/bin/env python3
"""
Test script to verify nochatbot functionality
"""
import sys
import asyncio
from pathlib import Path
import io

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add nochatbot to path
sys.path.insert(0, str(Path(__file__).parent))

from codewhisper.providers.glm import GLMProvider
from codewhisper.interaction.context import ConversationContext
from codewhisper.interaction.chatbot import IntelligentChatBot

async def test_glm_provider():
    """Test GLM provider"""
    print("Testing GLM Provider...")

    api_key = "4cb8fee1592944cdb31c5dacfb7515b4.uvONCflDVV6HHbW0"
    provider = GLMProvider(api_key=api_key, model="glm-4-plus")

    try:
        response = await provider.send_message(
            message="Hello, please respond with 'GLM is working!'",
            system_prompt="You are a helpful assistant.",
            temperature=0.7,
            max_tokens=100
        )
        print(f"✓ GLM Response: {response[:100]}")
        return True
    except Exception as e:
        print(f"✗ GLM Error: {e}")
        return False

async def test_context_and_chatbot():
    """Test ConversationContext and IntelligentChatBot"""
    print("\nTesting ConversationContext and ChatBot...")

    try:
        # Create context
        import uuid
        session_id = str(uuid.uuid4())
        context = ConversationContext(session_id=session_id)
        print(f"✓ Context created with session_id: {session_id[:8]}...")

        # Create chatbot
        api_key = "4cb8fee1592944cdb31c5dacfb7515b4.uvONCflDVV6HHbW0"
        provider = GLMProvider(api_key=api_key, model="glm-4-plus")

        project_info = {
            "path": "/test/project",
            "files_scanned": 3
        }

        chatbot = IntelligentChatBot(
            context=context,
            ai_provider=provider,
            project_info=project_info
        )
        print("✓ ChatBot created successfully")

        # Test chat
        response = await chatbot.chat("Say 'ChatBot is working!'", stream=False)
        print(f"✓ ChatBot Response: {response[:100]}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("="*60)
    print("No Chat Bot - Functionality Test")
    print("="*60)

    results = []

    # Test 1: GLM Provider
    results.append(await test_glm_provider())

    # Test 2: Context and ChatBot
    results.append(await test_context_and_chatbot())

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
