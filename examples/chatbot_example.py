"""Example usage of IntelligentChatBot with ConversationContext.

This example demonstrates how to:
1. Create a ConversationContext
2. Add user choices (selection history)
3. Initialize IntelligentChatBot with an AI provider
4. Use the chatbot with full context awareness
"""

import asyncio
from codewhisper.interaction import ConversationContext, IntelligentChatBot
from codewhisper.providers.base import AIProvider


# Example mock AI provider for demonstration
class MockAIProvider(AIProvider):
    """Mock AI provider for testing purposes."""

    async def send_message(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock send_message implementation."""
        return f"Mock response to: {message[:50]}..."

    async def stream_response(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock stream_response implementation."""
        response = f"Mock streaming response to: {message[:50]}..."
        for char in response:
            yield char

    def get_cost_per_token(self):
        """Mock cost calculation."""
        return {"input": 0.00001, "output": 0.00003}


async def main():
    """Demonstrate IntelligentChatBot usage."""

    # Step 1: Create a conversation context
    context = ConversationContext(
        session_id="demo-session-001",
        initial_mode="no_chat"
    )

    # Step 2: Simulate user making choices in no-chat mode
    print("=== Simulating No-Chat Mode Selections ===\n")

    context.add_choice(
        question="What type of project are you working on?",
        choice="Web Application",
        all_options=["Web Application", "Mobile App", "Desktop Software", "API Service"]
    )
    print("User selected: Web Application")

    context.add_choice(
        question="Which framework are you using?",
        choice="React",
        all_options=["React", "Vue", "Angular", "Svelte"]
    )
    print("User selected: React")

    context.add_choice(
        question="What issue are you facing?",
        choice="Performance optimization",
        all_options=["Performance optimization", "Bug fixing", "New feature", "Deployment"]
    )
    print("User selected: Performance optimization\n")

    # Step 3: Initialize the AI provider and chatbot
    print("=== Initializing IntelligentChatBot ===\n")

    ai_provider = MockAIProvider(api_key="mock-key", model="mock-model")

    project_info = {
        "project_name": "MyWebApp",
        "tech_stack": "React, Node.js, MongoDB",
        "team_size": "5 developers"
    }

    chatbot = IntelligentChatBot(
        context=context,
        ai_provider=ai_provider,
        project_info=project_info
    )

    # Step 4: User switches to chat mode and asks a question
    print("=== User Switches to Chat Mode ===\n")

    user_message = "Can you help me optimize my React components?"
    print(f"User: {user_message}\n")

    # Get response (this will automatically switch to chat mode)
    response = await chatbot.chat(user_message)
    print(f"Assistant: {response}\n")

    # Step 5: Continue the conversation
    print("=== Continuing Conversation ===\n")

    user_message_2 = "What about using React.memo?"
    print(f"User: {user_message_2}\n")

    response_2 = await chatbot.chat(user_message_2)
    print(f"Assistant: {response_2}\n")

    # Step 6: Display context summary
    print("=== Context Summary ===\n")
    summary = chatbot.get_context_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n=== Full Context Details ===\n")
    print(context.get_full_context_summary())

    # Step 7: Demonstrate system prompt building
    print("\n=== System Prompt (Internal) ===\n")
    system_prompt = chatbot._build_system_prompt()
    print(system_prompt)


if __name__ == "__main__":
    asyncio.run(main())
