"""
GRID Mistral Agent
==================

Initializes a Mistral agent with GRID-specific function definitions for:
- Pattern recognition and context analysis
- Discussion table comprehension (Great Hall)
- Decision logging and artifact generation
- Dynamic capability retrieval

Usage:
    python mistral_agent.py

Environment:
    MISTRAL_API_KEY: Mistral API key (required)
    MISTRAL_AGENT_ID: Agent ID (optional, uses default if not set)

Reference:
    - Function definitions: agents/function_definitions.py
    - Great Hall contract: OPEN_POLICY.md
    - Integration guide: README.md
"""

import os
import json
from typing import Optional, Any, List, Dict

from mistralai import Mistral

# Import GRID function definitions
try:
    from agents.function_definitions import (
        GRID_FUNCTION_REGISTRY,
        get_function_schemas_for_mistral,
        get_function_with_instructions,
    )
except ImportError:
    # Fallback for different import paths
    from .agents.function_definitions import (
        GRID_FUNCTION_REGISTRY,
        get_function_schemas_for_mistral,
        get_function_with_instructions,
    )


class GridMistralAgent:
    """Mistral agent configured with GRID capabilities."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        agent_id: Optional[str] = None,
        enable_functions: bool = True,
    ):
        """
        Initialize the GRID Mistral agent.

        Args:
            api_key: Mistral API key (defaults to MISTRAL_API_KEY env var)
            agent_id: Agent ID (defaults to MISTRAL_AGENT_ID env var)
            enable_functions: Whether to enable function calling (default: True)
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key not found. Set MISTRAL_API_KEY environment variable."
            )

        self.agent_id = agent_id or os.environ.get(
            "MISTRAL_AGENT_ID",
            "ag_019b213c8d2e70a3b17633c1c24e997a"  # Default agent ID
        )

        self.client = Mistral(api_key=self.api_key)
        self.enable_functions = enable_functions
        self.function_schemas = get_function_schemas_for_mistral() if enable_functions else []

    def get_system_prompt(self) -> str:
        """Get system prompt with GRID-specific instructions."""
        return """You are a GRID agent assistant specializing in:

1. **Pattern Recognition**: Analyze conversation for entities, relationships, and intent
2. **Discussion Comprehension**: Structure discussions into Great Hall decision tables
3. **Decision Logging**: Record decisions with rationale, bridges, and success metrics
4. **Data Validation**: Ensure content conforms to GRID/Great Hall schemas
5. **Artifact Generation**: Create canonical GRID artifacts (JSON contracts, reports, etc.)
6. **Capability Discovery**: Retrieve and initialize GRID subsystems on demand

Available Functions:
- analyze_grid_pattern: Extract entities and relationships
- validate_discussion_row: Check discussion rows for schema compliance
- log_decision_to_great_hall: Record decisions into Great Hall
- get_grid_capability: Retrieve GRID tools and services
- generate_grid_artifact: Create GRID artifacts in various formats

Instructions:
- Always use function calls when the user's intent maps to a GRID capability
- Provide GRID-specific context in your responses (references to schemas, contracts, etc.)
- When validating, reference the relevant constraint or standard (OPEN_POLICY.md, Great Hall contract)
- Be transparent about limitations and fallback behaviors
- Maintain traceability: always reference sources, decision IDs, or function calls used

Great Hall Tone:
- Default vibe: calm, direct, evidence-friendly
- Support all discussion vibes: nervous/high-stakes, exploratory/playful, analytical/methodical, restorative/repair
- Apply the "meet-halfway rule": advocate strongly + propose a bridge
"""

    def start_conversation(self, user_input: str) -> Dict[str, Any]:
        """
        Start a conversation with the agent.

        Args:
            user_input: User's initial message

        Returns:
            Response from agent
        """
        if not self.enable_functions:
            # Basic conversation without functions
            response = self.client.beta.conversations.start(
                agent_id=self.agent_id,
                inputs=user_input,
            )
            return self._format_response(response)

        # Conversation with function calling support
        messages = [
            {
                "role": "system",
                "content": self.get_system_prompt(),
            },
            {
                "role": "user",
                "content": user_input,
            }
        ]

        response = self.client.chat.complete(
            model="mistral-large-latest",  # Use latest model
            messages=messages,
            tools=self.function_schemas if self.enable_functions else None,
            tool_choice="auto" if self.enable_functions else None,
            temperature=0.7,
            max_tokens=2048,
        )

        return self._format_response(response)

    def continue_conversation(
        self,
        conversation_id: str,
        user_input: str,
    ) -> Dict[str, Any]:
        """
        Continue an existing conversation.

        Args:
            conversation_id: ID of existing conversation
            user_input: User's next message

        Returns:
            Response from agent
        """
        response = self.client.beta.conversations.continue_conversation(
            conversation_id=conversation_id,
            inputs=user_input,
        )
        return self._format_response(response)

    def _format_response(self, response: Any) -> Dict[str, Any]:
        """Format agent response into structured dict."""
        return {
            "status": "success" if hasattr(response, "choices") else "pending",
            "response": str(response),
            "raw": response,
        }

    def list_available_functions(self) -> Dict[str, Any]:
        """Get list of available GRID functions with full instructions."""
        return {
            func_name: get_function_with_instructions(func_name)
            for func_name in GRID_FUNCTION_REGISTRY.keys()
        }


def main():
    """Run agent in interactive mode."""
    agent = GridMistralAgent(enable_functions=True)

    print("=" * 70)
    print("GRID Mistral Agent - Interactive Mode")
    print("=" * 70)
    print(f"Agent ID: {agent.agent_id}")
    print(f"Functions Enabled: {agent.enable_functions}")
    print(f"Available Functions: {len(agent.function_schemas)}")
    print("\nType 'help' for function list, 'quit' to exit")
    print("-" * 70)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            if user_input.lower() == "help":
                functions = agent.list_available_functions()
                print("\nAvailable GRID Functions:")
                for func_name, func_info in functions.items():
                    print(f"\n  {func_name}:")
                    print(f"    {func_info['description']}")
                    print(f"    Type: {func_info.get('type', 'unknown')}")
                continue

            print("\nAgent: Processing...")
            response = agent.start_conversation(user_input)

            if response["status"] == "success":
                print(f"Agent Response:\n{response['response']}")
            else:
                print(f"Agent Status: {response['status']}\n{response['response']}")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
