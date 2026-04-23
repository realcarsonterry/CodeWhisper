"""Interactive interface for CodeWhisper system.

This module provides the main interactive interface that manages the user experience,
switching between No Chat mode (question-based navigation) and Chat mode (free conversation).
"""

import asyncio
import uuid
from typing import Optional, Dict, Any
import click

from codewhisper.interaction.context import ConversationContext
from codewhisper.interaction.chatbot import IntelligentChatBot
from codewhisper.recommendation.question_generator import QuestionGenerator
from codewhisper.providers.base import AIProvider


class InteractiveInterface:
    """Main interactive interface for CodeWhisper.

    This class manages the user interaction flow, providing:
    - No Chat mode: Question-based navigation with 8 options + mode switch
    - Chat mode: Free conversation with /back and /exit commands
    - Seamless context preservation across mode switches
    """

    def __init__(
        self,
        ai_provider: AIProvider,
        project_info: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ):
        """Initialize the interactive interface.

        Args:
            ai_provider: AI provider instance for generating responses
            project_info: Optional project information for context
            session_id: Optional session ID (generated if not provided)
        """
        self.ai_provider = ai_provider
        self.project_info = project_info or {}
        self.session_id = session_id or str(uuid.uuid4())

        # Initialize components
        self.context = ConversationContext(
            session_id=self.session_id,
            initial_mode="no_chat"
        )
        self.question_generator = QuestionGenerator(ai_provider)
        self.chatbot = IntelligentChatBot(
            context=self.context,
            ai_provider=ai_provider,
            project_info=project_info
        )

        self.running = True

    def start(self) -> None:
        """Start the interactive interface.

        This is the main entry point that begins the interaction loop.
        It starts in No Chat mode by default.
        """
        click.clear()
        self._print_welcome()

        # Run the async event loop
        asyncio.run(self._main_loop())

    async def _main_loop(self) -> None:
        """Main interaction loop.

        Manages the flow between No Chat and Chat modes based on
        the current context mode.
        """
        while self.running:
            try:
                if self.context.mode == "no_chat":
                    await self._no_chat_mode()
                else:
                    await self._chat_mode()
            except KeyboardInterrupt:
                self._handle_exit()
                break
            except Exception as e:
                click.echo(click.style(f"\nError: {str(e)}", fg="red"))
                click.echo("Please try again or type /exit to quit.\n")

    async def _no_chat_mode(self) -> None:
        """No Chat mode: Display question with 8 options + mode switch.

        This mode:
        1. Generates 8 intelligent options based on context
        2. Displays them with descriptions
        3. Adds a 9th option to switch to Chat mode
        4. Records user selection to context
        """
        click.echo()
        click.echo(click.style("=" * 70, fg="cyan"))
        click.echo(click.style("No Chat Mode", fg="cyan", bold=True))
        click.echo(click.style("=" * 70, fg="cyan"))
        click.echo()

        # Generate questions based on current context
        try:
            context_data = self._build_question_context()
            result = await self.question_generator.generate_questions(context_data)
        except Exception as e:
            click.echo(click.style(f"Failed to generate questions: {e}", fg="red"))

            # Check if we have alternative providers
            if hasattr(self, 'all_providers') and len(self.all_providers) > 1:
                click.echo(click.style("\n检测到您配置了多个 API 提供商。", fg="yellow"))
                click.echo("当前使用的 API 可能余额不足或不可用。\n")

                # Show available providers
                click.echo(click.style("可用的 API 提供商:", fg="cyan"))
                for i, provider in enumerate(self.all_providers, 1):
                    provider_name = provider.__class__.__name__.replace('Provider', '')
                    click.echo(f"  [{i}] {provider_name} - {provider.model}")

                click.echo()
                if click.confirm("是否尝试切换到其他 API 提供商?", default=True):
                    choice = click.prompt("请选择提供商编号", type=int, default=1)
                    if 1 <= choice <= len(self.all_providers):
                        self.ai_provider = self.all_providers[choice - 1]
                        self.question_generator.ai_provider = self.ai_provider
                        self.chatbot.ai_provider = self.ai_provider

                        provider_name = self.ai_provider.__class__.__name__.replace('Provider', '')
                        click.echo(click.style(f"\n✓ 已切换到 {provider_name}", fg="green"))
                        click.echo("正在重新生成问题...\n")

                        # Retry with new provider
                        try:
                            result = await self.question_generator.generate_questions(context_data)
                        except Exception as retry_error:
                            click.echo(click.style(f"切换后仍然失败: {retry_error}", fg="red"))
                            click.echo("请检查 API 配置或稍后重试。")
                            self._handle_exit()
                            return
                    else:
                        click.echo(click.style("无效的选择", fg="red"))
                        self._handle_exit()
                        return
                else:
                    click.echo("请检查 API 配置或稍后重试。")
                    self._handle_exit()
                    return
            else:
                click.echo("请检查 API 配置或稍后重试。")
                self._handle_exit()
                return

        # Display question
        click.echo(click.style(result.question, fg="yellow", bold=True))
        click.echo()

        # Display 8 options
        for option in result.options:
            option_id = click.style(f"[{option['id']}]", fg="green", bold=True)
            option_text = click.style(option['text'], fg="white", bold=True)
            option_desc = click.style(option['description'], fg="bright_black")

            click.echo(f"{option_id} {option_text}")
            click.echo(f"    {option_desc}")
            click.echo()

        # Display 9th option: Switch to Chat mode
        chat_option = click.style("[9]", fg="magenta", bold=True)
        chat_text = click.style("Switch to Chat Mode", fg="white", bold=True)
        chat_desc = click.style("Have a free conversation with the AI assistant", fg="bright_black")

        click.echo(f"{chat_option} {chat_text}")
        click.echo(f"    {chat_desc}")
        click.echo()

        # Get user input
        click.echo(click.style("─" * 70, fg="cyan"))
        choice = click.prompt(
            click.style("Your choice", fg="cyan"),
            type=str,
            default="",
            show_default=False
        ).strip()

        # Handle user choice
        if choice == "9":
            # Switch to Chat mode
            self.context.switch_to_chat("User selected Chat mode")
            click.echo(click.style("\nSwitching to Chat mode...", fg="magenta"))
        elif choice in [opt['id'] for opt in result.options]:
            # Record the selection
            selected_option = next(opt for opt in result.options if opt['id'] == choice)
            all_option_texts = [opt['text'] for opt in result.options]

            self.context.add_choice(
                question=result.question,
                choice=selected_option['text'],
                all_options=all_option_texts
            )

            click.echo(click.style(f"\nYou selected: {selected_option['text']}", fg="green"))
            click.echo("Processing your selection...\n")

            # Here you could add logic to process the selection
            # For now, we continue to the next question

        elif choice.lower() in ['/exit', 'exit', 'quit']:
            self._handle_exit()
        else:
            click.echo(click.style("\nInvalid choice. Please select a valid option number.", fg="red"))

    async def _chat_mode(self) -> None:
        """Chat mode: Free conversation with AI assistant.

        This mode:
        1. Accepts user messages
        2. Supports /back to return to No Chat mode
        3. Supports /exit to quit
        4. Processes messages through IntelligentChatBot
        5. Maintains conversation history
        """
        click.echo()
        click.echo(click.style("=" * 70, fg="magenta"))
        click.echo(click.style("Chat Mode", fg="magenta", bold=True))
        click.echo(click.style("=" * 70, fg="magenta"))
        click.echo()

        # Show help message
        click.echo(click.style("You can now chat freely with the AI assistant.", fg="bright_black"))
        click.echo(click.style("Commands: /back (return to No Chat mode), /exit (quit)", fg="bright_black"))
        click.echo()

        # Get user input
        click.echo(click.style("─" * 70, fg="magenta"))
        user_message = click.prompt(
            click.style("You", fg="cyan", bold=True),
            type=str,
            default="",
            show_default=False
        ).strip()

        # Handle commands
        if user_message.lower() == '/back':
            self.context.switch_to_no_chat("User requested to go back")
            click.echo(click.style("\nReturning to No Chat mode...", fg="magenta"))
            return

        if user_message.lower() in ['/exit', 'exit', 'quit']:
            self._handle_exit()
            return

        if not user_message:
            click.echo(click.style("Please enter a message or command.", fg="red"))
            return

        # Process message through chatbot
        try:
            click.echo()
            click.echo(click.style("Assistant: ", fg="green", bold=True), nl=False)

            # Stream the response for better UX
            response_text = ""
            async for chunk in self.chatbot.chat(user_message, stream=True):
                click.echo(chunk, nl=False)
                response_text += chunk

            click.echo()  # New line after response
            click.echo()

        except Exception as e:
            click.echo(click.style(f"\nError processing message: {e}", fg="red"))
            click.echo("Please try again.\n")

    def _build_question_context(self) -> Dict[str, Any]:
        """Build context for question generation.

        Returns:
            Dictionary containing context information for the question generator
        """
        # Determine context type
        if not self.context.choice_history and not self.context.chat_history:
            # First time interaction
            context_type = 'first_time'
            context_data = {
                'type': context_type,
                'scan_results': self.project_info.get('scan_results', {})
            }
        elif self.context.mode_switches and self.context.mode_switches[-1].from_mode == "chat":
            # Coming back from chat mode
            context_type = 'from_chat'
            chat_content = [
                {'role': msg.role, 'content': msg.content}
                for msg in self.context.chat_history
            ]
            context_data = {
                'type': context_type,
                'chat_content': chat_content,
                'knowledge_base': list(self.context.knowledge_base.values())
            }
        else:
            # Subsequent interaction
            context_type = 'subsequent'
            selection_history = [
                {
                    'question': choice.question,
                    'selected_option': {
                        'text': choice.choice,
                        'all_options': choice.all_options
                    }
                }
                for choice in self.context.choice_history
            ]
            context_data = {
                'type': context_type,
                'selection_history': selection_history,
                'knowledge_base': list(self.context.knowledge_base.values())
            }

        return context_data

    def _print_welcome(self) -> None:
        """Print welcome message."""
        click.echo()
        click.echo(click.style("╔" + "═" * 68 + "╗", fg="cyan", bold=True))
        click.echo(click.style("║" + " " * 68 + "║", fg="cyan", bold=True))
        click.echo(
            click.style("║", fg="cyan", bold=True) +
            click.style("  Welcome to CodeWhisper - Intelligent Code Assistant  ", fg="yellow", bold=True) +
            click.style("║", fg="cyan", bold=True)
        )
        click.echo(click.style("║" + " " * 68 + "║", fg="cyan", bold=True))
        click.echo(click.style("╚" + "═" * 68 + "╝", fg="cyan", bold=True))
        click.echo()
        click.echo(click.style("Session ID: ", fg="bright_black") + click.style(self.session_id, fg="white"))

        if self.project_info.get('project_name'):
            click.echo(
                click.style("Project: ", fg="bright_black") +
                click.style(self.project_info['project_name'], fg="white")
            )

        click.echo()

    def _handle_exit(self) -> None:
        """Handle exit command."""
        self.running = False
        click.echo()
        click.echo(click.style("=" * 70, fg="cyan"))
        click.echo(click.style("Thank you for using CodeWhisper!", fg="yellow", bold=True))
        click.echo()

        # Show session summary
        summary = self.chatbot.get_context_summary()
        click.echo(click.style("Session Summary:", fg="cyan", bold=True))
        click.echo(f"  Total selections: {summary['total_choices']}")
        click.echo(f"  Total messages: {summary['total_chat_messages']}")
        click.echo(f"  Mode switches: {summary['total_mode_switches']}")
        click.echo()
        click.echo(click.style("=" * 70, fg="cyan"))
        click.echo()

    def get_context(self) -> ConversationContext:
        """Get the current conversation context.

        Returns:
            The ConversationContext instance
        """
        return self.context

    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session.

        Returns:
            Dictionary containing session summary information
        """
        return self.chatbot.get_context_summary()
