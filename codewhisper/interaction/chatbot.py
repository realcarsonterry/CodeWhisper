"""Intelligent Chat Bot with context awareness."""

from typing import Dict, Any, Optional
from codewhisper.interaction.context import ConversationContext
from codewhisper.providers.base import AIProvider


class IntelligentChatBot:
    """Intelligent Chat Bot that inherits context from CodeWhisper.

    This class provides AI-powered chat functionality with full awareness of
    the user's selection history and previous conversations. It uses the context
    to provide precise, contextual assistance.
    """

    def __init__(self, context: ConversationContext, ai_provider: AIProvider, project_info: Optional[Dict[str, Any]] = None):
        """Initialize the Intelligent Chat Bot.

        Args:
            context: ConversationContext instance containing selection and chat history
            ai_provider: AI provider instance for generating responses
            project_info: Optional project information for additional context
        """
        self.context = context
        self.ai_provider = ai_provider
        self.project_info = project_info or {}
        self.knowledge_base_summary: Optional[str] = None

    async def chat(self, user_message: str, stream: bool = False):
        """Process a user message and generate a response.

        Args:
            user_message: The user's message
            stream: Whether to stream the response (default: False)

        Returns:
            The AI's response text if stream=False, or an async generator if stream=True
        """
        if stream:
            return self._chat_stream(user_message)
        else:
            return await self._chat_normal(user_message)

    async def _chat_normal(self, user_message: str) -> str:
        """Process a user message and return the complete response.

        Args:
            user_message: The user's message

        Returns:
            The AI's response text
        """
        # Switch to chat mode if not already
        if self.context.mode != "chat":
            self.context.switch_to_chat("User initiated chat")

        # Add user message to chat history
        self.context.add_chat_message("user", user_message)

        # Build system prompt with full context
        system_prompt = self._build_system_prompt()

        # Build message history
        messages = self._build_messages(user_message)

        # Get response from AI provider
        response = await self.ai_provider.send_message(
            message=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2048
        )

        # Add assistant response to chat history
        self.context.add_chat_message("assistant", response)

        return response

    async def _chat_stream(self, user_message: str):
        """Process a user message and stream the response.

        Args:
            user_message: The user's message

        Yields:
            Response chunks
        """
        # Switch to chat mode if not already
        if self.context.mode != "chat":
            self.context.switch_to_chat("User initiated chat")

        # Add user message to chat history
        self.context.add_chat_message("user", user_message)

        # Build system prompt with full context
        system_prompt = self._build_system_prompt()

        # Build message history
        messages = self._build_messages(user_message)

        # Stream response from AI provider
        response_text = ""
        async for chunk in self.ai_provider.stream_response(
            message=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2048
        ):
            response_text += chunk
            yield chunk

        # Add assistant response to chat history
        self.context.add_chat_message("assistant", response_text)

    def _build_system_prompt(self) -> str:
        """Build the system prompt with complete context.

        The system prompt includes:
        - User's selection path (question-answer history)
        - Chat conversation history
        - Project information
        - Knowledge base summary
        - Instructions for the AI on how to respond

        Returns:
            Complete system prompt string
        """
        prompt_parts = []

        # Role and purpose
        prompt_parts.append(
            "You are an intelligent assistant for the CodeWhisper system. "
            "Your role is to help users based on their selection history and provide precise, contextual assistance."
        )

        # User's selection path
        if self.context.choice_history:
            prompt_parts.append("\n## User's Selection Path")
            prompt_parts.append("The user has made the following selections through the question-based navigation:")
            for i, choice in enumerate(self.context.choice_history, 1):
                prompt_parts.append(f"\n{i}. Q: {choice.question}")
                prompt_parts.append(f"   A: {choice.choice}")
                prompt_parts.append(f"   (Options were: {', '.join(choice.all_options)})")
            prompt_parts.append("\nUse this selection path to understand the user's intent and context.")

        # Project information
        if self.project_info:
            prompt_parts.append("\n## Project Information")
            for key, value in self.project_info.items():
                prompt_parts.append(f"- {key}: {value}")

        # Knowledge base summary
        if self.knowledge_base_summary:
            prompt_parts.append("\n## Knowledge Base Summary")
            prompt_parts.append(self.knowledge_base_summary)
        elif self.context.knowledge_base:
            prompt_parts.append("\n## Knowledge Base")
            for key, value in self.context.knowledge_base.items():
                prompt_parts.append(f"- {key}: {value}")

        # Chat history context
        if self.context.chat_history:
            prompt_parts.append("\n## Previous Conversation")
            prompt_parts.append(f"There have been {len(self.context.chat_history)} messages exchanged so far.")
            prompt_parts.append("The conversation history is included in the messages below.")

        # Mode switches context
        if self.context.mode_switches:
            prompt_parts.append("\n## Mode Switches")
            prompt_parts.append(f"The user has switched between modes {len(self.context.mode_switches)} times.")

        # Instructions
        prompt_parts.append("\n## Instructions")
        prompt_parts.append(
            "- Provide precise, helpful responses based on the user's selection path and conversation history\n"
            "- Reference specific selections when relevant to show understanding of context\n"
            "- Be concise but thorough in your explanations\n"
            "- If the user's question relates to their previous selections, acknowledge that connection\n"
            "- Offer actionable advice and next steps when appropriate\n"
            "- If you need more information, ask clarifying questions"
        )

        return "\n".join(prompt_parts)

    def _build_messages(self, user_message: str) -> str:
        """Build the message history for the AI provider.

        Args:
            user_message: The current user message

        Returns:
            Formatted message string or list depending on provider requirements
        """
        # For simple providers that expect a single message string,
        # we include recent chat history in the message
        if not self.context.chat_history:
            return user_message

        # Include recent conversation history (last 10 messages)
        recent_history = self.context.chat_history[-10:]

        message_parts = []
        if len(recent_history) > 1:  # More than just the current message
            message_parts.append("Recent conversation:")
            for msg in recent_history[:-1]:  # Exclude the current message we just added
                role_label = "User" if msg.role == "user" else "Assistant"
                message_parts.append(f"{role_label}: {msg.content}")
            message_parts.append(f"\nCurrent message: {user_message}")
            return "\n".join(message_parts)

        return user_message

    def _summarize_kb(self) -> str:
        """Summarize the knowledge base for context.

        This method would typically query a vector database or knowledge base
        to get relevant information based on the user's selection path.

        Returns:
            Summary of relevant knowledge base content
        """
        # Placeholder implementation
        # In a full implementation, this would:
        # 1. Query the knowledge base based on selection history
        # 2. Retrieve relevant documents/information
        # 3. Summarize the findings

        if not self.context.choice_history:
            return "No specific knowledge base context available."

        # Extract key topics from selection history
        topics = []
        for choice in self.context.choice_history:
            topics.append(choice.choice)

        summary = f"Knowledge base context related to: {', '.join(topics)}"
        return summary

    def set_knowledge_base_summary(self, summary: str) -> None:
        """Set the knowledge base summary manually.

        Args:
            summary: Pre-computed knowledge base summary
        """
        self.knowledge_base_summary = summary

    def update_project_info(self, info: Dict[str, Any]) -> None:
        """Update project information.

        Args:
            info: Dictionary of project information to merge
        """
        self.project_info.update(info)

    def get_context_summary(self) -> Dict[str, Any]:
        """Get a complete summary of the current context.

        Returns:
            Dictionary containing all context information
        """
        return {
            "session_id": self.context.session_id,
            "mode": self.context.mode,
            "project_info": self.project_info,
            "knowledge_base_summary": self.knowledge_base_summary,
            "total_choices": len(self.context.choice_history),
            "total_chat_messages": len(self.context.chat_history),
            "total_mode_switches": len(self.context.mode_switches),
            "current_depth": self.context.current_depth
        }

    def clear_chat_history(self) -> None:
        """Clear only the chat history, preserving selection history."""
        self.context.chat_history.clear()

    def reset(self) -> None:
        """Reset all context including selections and chat history."""
        self.context.choice_history.clear()
        self.context.chat_history.clear()
        self.context.mode_switches.clear()
        self.context.knowledge_base.clear()
        self.context.current_depth = 0
        self.knowledge_base_summary = None
