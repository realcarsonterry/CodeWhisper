"""Conversation context management for No Chat Bot."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Literal


@dataclass
class Choice:
    """Represents a user choice in no-chat mode.

    Attributes:
        question: The question that was asked
        choice: The option that was selected
        all_options: All available options at the time
        timestamp: When the choice was made
    """
    question: str
    choice: str
    all_options: List[str]
    timestamp: datetime


@dataclass
class ChatMessage:
    """Represents a chat message.

    Attributes:
        role: The role of the message sender (user or assistant)
        content: The message content
        timestamp: When the message was sent
    """
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime


@dataclass
class ModeSwitch:
    """Represents a mode switch event.

    Attributes:
        from_mode: The mode being switched from
        to_mode: The mode being switched to
        reason: The reason for the switch
        timestamp: When the switch occurred
    """
    from_mode: Literal["no_chat", "chat"]
    to_mode: Literal["no_chat", "chat"]
    reason: str
    timestamp: datetime


class ConversationContext:
    """Manages conversation context across no-chat and chat modes.

    This class tracks the entire conversation history including user choices,
    chat messages, mode switches, and maintains a knowledge base of learned
    information. It provides methods to add new interactions and generate
    context summaries.

    Attributes:
        session_id: Unique identifier for this conversation session
        mode: Current interaction mode ("no_chat" or "chat")
        choice_history: List of all choices made in no-chat mode
        chat_history: List of all chat messages
        knowledge_base: Dictionary storing learned information
        current_depth: Current depth in the decision tree
        mode_switches: History of mode switches
    """

    def __init__(
        self,
        session_id: str,
        initial_mode: Literal["no_chat", "chat"] = "no_chat"
    ) -> None:
        """Initialize a new conversation context.

        Args:
            session_id: Unique identifier for this session
            initial_mode: Starting mode (defaults to "no_chat")
        """
        self.session_id: str = session_id
        self.mode: Literal["no_chat", "chat"] = initial_mode
        self.choice_history: List[Choice] = []
        self.chat_history: List[ChatMessage] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.current_depth: int = 0
        self.mode_switches: List[ModeSwitch] = []

    def add_choice(
        self,
        question: str,
        choice: str,
        all_options: List[str]
    ) -> None:
        """Add a user choice to the history.

        Args:
            question: The question that was asked
            choice: The option that was selected
            all_options: All available options at the time
        """
        choice_record = Choice(
            question=question,
            choice=choice,
            all_options=all_options,
            timestamp=datetime.now()
        )
        self.choice_history.append(choice_record)
        self.current_depth += 1

    def add_chat_message(
        self,
        role: Literal["user", "assistant"],
        content: str
    ) -> None:
        """Add a chat message to the history.

        Args:
            role: The role of the message sender ("user" or "assistant")
            content: The message content
        """
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now()
        )
        self.chat_history.append(message)

    def switch_to_chat(self, reason: str) -> None:
        """Switch from no-chat mode to chat mode.

        Args:
            reason: The reason for switching to chat mode
        """
        if self.mode != "chat":
            switch = ModeSwitch(
                from_mode=self.mode,
                to_mode="chat",
                reason=reason,
                timestamp=datetime.now()
            )
            self.mode_switches.append(switch)
            self.mode = "chat"

    def switch_to_no_chat(self, reason: str) -> None:
        """Switch from chat mode to no-chat mode.

        Args:
            reason: The reason for switching to no-chat mode
        """
        if self.mode != "no_chat":
            switch = ModeSwitch(
                from_mode=self.mode,
                to_mode="no_chat",
                reason=reason,
                timestamp=datetime.now()
            )
            self.mode_switches.append(switch)
            self.mode = "no_chat"

    def get_full_context_summary(self) -> str:
        """Generate a complete summary of the conversation context.

        Returns:
            A formatted string containing the full context summary including
            session info, choice history, chat history, mode switches, and
            knowledge base.
        """
        lines = [
            f"Session ID: {self.session_id}",
            f"Current Mode: {self.mode}",
            f"Current Depth: {self.current_depth}",
            f"Total Choices: {len(self.choice_history)}",
            f"Total Messages: {len(self.chat_history)}",
            f"Mode Switches: {len(self.mode_switches)}",
            ""
        ]

        if self.choice_history:
            lines.append("=== Choice History ===")
            for i, choice in enumerate(self.choice_history, 1):
                lines.append(f"{i}. [{choice.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]")
                lines.append(f"   Q: {choice.question}")
                lines.append(f"   A: {choice.choice}")
                lines.append(f"   Options: {', '.join(choice.all_options)}")
            lines.append("")

        if self.chat_history:
            lines.append("=== Chat History ===")
            for msg in self.chat_history:
                timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                lines.append(f"[{timestamp}] {msg.role.upper()}: {msg.content}")
            lines.append("")

        if self.mode_switches:
            lines.append("=== Mode Switches ===")
            for switch in self.mode_switches:
                timestamp = switch.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                lines.append(
                    f"[{timestamp}] {switch.from_mode} -> {switch.to_mode}: "
                    f"{switch.reason}"
                )
            lines.append("")

        if self.knowledge_base:
            lines.append("=== Knowledge Base ===")
            for key, value in self.knowledge_base.items():
                lines.append(f"{key}: {value}")
            lines.append("")

        return "\n".join(lines)

    def get_recent_chat_summary(self, last_n: int = 5) -> str:
        """Generate a summary of recent chat messages.

        Args:
            last_n: Number of recent messages to include (default: 5)

        Returns:
            A formatted string containing the recent chat messages
        """
        if not self.chat_history:
            return "No chat history available."

        recent_messages = self.chat_history[-last_n:]
        lines = [f"=== Recent Chat (Last {len(recent_messages)} messages) ==="]

        for msg in recent_messages:
            timestamp = msg.timestamp.strftime('%H:%M:%S')
            lines.append(f"[{timestamp}] {msg.role.upper()}: {msg.content}")

        return "\n".join(lines)
