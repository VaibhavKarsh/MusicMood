"""
Agent 1: Mood Understanding Agent
Uses LangChain ReAct pattern to analyze user mood and extract structured data.
"""

import logging
from typing import Dict, Any, Optional, List

from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.tools.mood_tools import parse_mood_tool, get_mood_description
from app.tools.user_tools import create_get_user_context_tool

logger = logging.getLogger(__name__)


# Agent prompt template
MOOD_AGENT_PROMPT = """You are a Mood Understanding Agent. Your job is to analyze user mood input and extract structured mood data.

You have access to the following tools:

{tools}

Tool Names: {tool_names}

Use the following format:

Question: the input question or task you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT:
- Always use parse_mood_with_llm to analyze the user's mood text
- If you have a user_id, use get_user_context to understand their preferences
- Your final answer should be the JSON mood data from parse_mood_with_llm
- Be concise and focused on extracting mood data

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


class MoodUnderstandingAgent:
    """
    Agent that understands and structures user mood input.
    """

    def __init__(self, db_session: Optional[Session] = None):
        """
        Initialize the Mood Understanding Agent.

        Args:
            db_session: Optional database session for user context retrieval
        """

        self.db_session = db_session

        # Initialize LLM
        self.llm = OllamaLLM(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.3,  # Lower temperature for more consistent parsing
            num_predict=settings.OLLAMA_MAX_TOKENS,
        )

        # Setup tools
        self.tools = self._setup_tools()

        # Create prompt
        self.prompt = PromptTemplate(
            template=MOOD_AGENT_PROMPT,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": self._format_tools(),
                "tool_names": ", ".join([tool.name for tool in self.tools])
            }
        )

        # Create agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=settings.AGENT_VERBOSE,
            max_iterations=settings.AGENT_MAX_ITERATIONS,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

        logger.info(f"Mood Understanding Agent initialized with {len(self.tools)} tools")

    def _setup_tools(self) -> List[Tool]:
        """Setup tools for the agent."""

        tools = [parse_mood_tool]

        # Add user context tool if database session is available
        if self.db_session:
            user_context_tool = create_get_user_context_tool(self.db_session)
            tools.append(user_context_tool)

        return tools

    def _format_tools(self) -> str:
        """Format tools for the prompt."""
        tool_strings = []
        for tool in self.tools:
            tool_strings.append(f"- {tool.name}: {tool.description}")
        return "\n".join(tool_strings)

    def analyze_mood(
        self,
        mood_text: str,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Analyze user mood and return structured data.

        Args:
            mood_text: User's mood description
            user_id: Optional user ID for context

        Returns:
            Dictionary with mood data and agent reasoning
        """

        logger.info(f"Analyzing mood: {mood_text[:100]}...")

        try:
            # Build input
            agent_input = f"Analyze this mood: '{mood_text}'"

            if user_id and self.db_session:
                agent_input += f" (User ID: {user_id})"

            # Run agent
            result = self.agent_executor.invoke({"input": agent_input})

            # Extract mood data from final answer
            import json
            mood_data = json.loads(result["output"])

            # Add agent metadata
            response = {
                "mood_data": mood_data,
                "agent_steps": len(result.get("intermediate_steps", [])),
                "reasoning": self._extract_reasoning(result),
                "success": True
            }

            logger.info(f"Mood analysis complete: {mood_data.get('primary_mood')}")
            return response

        except Exception as e:
            logger.error(f"Error in mood analysis: {e}")

            # Return fallback
            import json
            fallback_mood = json.dumps({
                "primary_mood": "calm",
                "energy_level": 5,
                "emotional_intensity": 5,
                "context": "general",
                "mood_tags": ["neutral"]
            })

            return {
                "mood_data": json.loads(fallback_mood),
                "agent_steps": 0,
                "reasoning": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }

    def _extract_reasoning(self, result: Dict) -> str:
        """Extract agent reasoning from result."""

        steps = result.get("intermediate_steps", [])

        if not steps:
            return "No reasoning steps"

        reasoning_parts = []
        for action, observation in steps:
            reasoning_parts.append(f"Tool: {action.tool}, Input: {action.tool_input[:100]}")

        return " | ".join(reasoning_parts)


# Factory function
def create_mood_agent(db_session: Optional[Session] = None) -> MoodUnderstandingAgent:
    """
    Create a Mood Understanding Agent instance.

    Args:
        db_session: Optional database session

    Returns:
        MoodUnderstandingAgent instance
    """
    return MoodUnderstandingAgent(db_session=db_session)
