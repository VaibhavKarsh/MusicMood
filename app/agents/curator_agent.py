"""
Agent 3: Playlist Curator Agent

This agent uses the ReAct pattern to curate personalized playlists by:
1. Ranking tracks by relevance to mood
2. Optimizing for diversity
3. Generating explanations for the curation
"""

import logging
from typing import Dict, Any, Optional, List
import json

from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

from app.config.settings import settings
from app.tools.curator_tools import (
    rank_tracks_tool,
    optimize_diversity_tool,
    generate_explanation_tool
)

logger = logging.getLogger(__name__)


# Agent 3 Prompt Template
CURATOR_AGENT_PROMPT = """You are an expert music curator AI that MUST use tools to curate playlists.

CRITICAL: You MUST use ALL THREE tools in the exact order specified. Do NOT create playlists manually.

Your workflow:
1. FIRST: Use rank_tracks_by_relevance to score all candidate tracks
2. SECOND: Use optimize_diversity to select final tracks with diversity constraints
3. THIRD: Use generate_explanation to create the explanation

You have access to these tools:

{tools}

Tool Names: {tool_names}

STRICT RULES:
- You MUST call rank_tracks_by_relevance FIRST
- You MUST call optimize_diversity SECOND  
- You MUST call generate_explanation THIRD
- Do NOT skip any tools
- Do NOT create playlists manually
- Use the EXACT tool outputs as your final answer

Use this format:

Question: the input question you must answer
Thought: I need to use rank_tracks_by_relevance first
Action: rank_tracks_by_relevance
Action Input: the JSON inputs for ranking
Observation: the result of the action
Thought: Now I need to use optimize_diversity
Action: optimize_diversity  
Action Input: the ranked tracks from previous step
Observation: the result of the action
Thought: Finally I need to use generate_explanation
Action: generate_explanation
Action Input: the playlist from previous step
Observation: the result of the action
Thought: I now have the complete curated playlist
Final Answer: [Return the complete JSON from the last tool]

Begin!

Question: {input}
Thought:{agent_scratchpad}"""


class PlaylistCuratorAgent:
    """
    Agent 3: Playlist Curator
    
    This agent takes candidate tracks and mood data, then curates
    a personalized playlist using ranking, diversity optimization,
    and explanation generation.
    """
    
    def __init__(self):
        """Initialize the Playlist Curator Agent."""
        try:
            # Initialize Ollama LLM
            self.llm = Ollama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0.3  # Lower temperature for more consistent curation
            )
            
            # Define tools
            self.tools = [
                rank_tracks_tool,
                optimize_diversity_tool,
                generate_explanation_tool
            ]
            
            # Create prompt template
            self.prompt = PromptTemplate.from_template(CURATOR_AGENT_PROMPT)
            
            # Create agent
            self.agent = create_react_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=self.prompt
            )
            
            # Create executor
            self.executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                max_iterations=5,  # Allow up to 5 iterations
                handle_parsing_errors=True,
                return_intermediate_steps=True
            )
            
            logger.info("Playlist Curator Agent initialized with 3 tools")
            
        except Exception as e:
            logger.error(f"Error initializing Playlist Curator Agent: {e}")
            raise
    
    def curate_playlist(
        self,
        candidate_tracks: List[Dict[str, Any]],
        mood_data: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None,
        desired_count: int = 30
    ) -> Dict[str, Any]:
        """
        Curate a personalized playlist from candidate tracks.
        
        Args:
            candidate_tracks: List of track dictionaries with audio features
            mood_data: Mood data from Agent 1
            user_context: Optional user preferences and history
            desired_count: Number of tracks for final playlist (default 30)
            
        Returns:
            Dictionary with:
            - playlist: List of curated tracks
            - explanation: Natural language explanation
            - diversity_metrics: Diversity statistics
            - execution_time: Time taken to curate
        """
        import time
        start_time = time.time()
        
        try:
            logger.info(f"Curating playlist from {len(candidate_tracks)} candidates for mood: {mood_data.get('primary_mood')}")
            
            # Prepare input for agent
            input_data = {
                "candidate_tracks": candidate_tracks,
                "mood_data": mood_data,
                "user_context": user_context or {},
                "desired_count": desired_count
            }
            
            # Create agent input question
            question = f"""Curate a {desired_count}-track playlist for {mood_data.get('primary_mood')} mood.

You MUST follow these steps exactly:

Step 1: Call rank_tracks_by_relevance
tracks_json={json.dumps(candidate_tracks)}
mood_data_json={json.dumps(mood_data)}
user_context_json={json.dumps(user_context or {})}

Step 2: Call optimize_diversity
ranked_tracks_json=(output from step 1)
desired_count={desired_count}

Step 3: Call generate_explanation
playlist_json=(output from step 2)
mood_data_json={json.dumps(mood_data)}

Do NOT skip any steps. Use ALL tools."""
            
            # Execute agent
            logger.info("Executing Playlist Curator Agent...")
            result = self.executor.invoke({"input": question})
            
            execution_time = time.time() - start_time
            
            # Extract results
            final_answer = result.get('output', '')
            intermediate_steps = result.get('intermediate_steps', [])
            
            logger.info(f"Agent completed curation in {execution_time:.2f}s")
            logger.info(f"Agent took {len(intermediate_steps)} steps")
            
            # Parse final answer to extract playlist and explanation
            parsed_result = self._parse_agent_output(final_answer, intermediate_steps)
            parsed_result['execution_time'] = round(execution_time, 2)
            parsed_result['curation_strategy'] = self._extract_strategy(intermediate_steps)
            
            logger.info(f"Curated playlist with {len(parsed_result.get('playlist', []))} tracks")
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"Error curating playlist: {e}")
            execution_time = time.time() - start_time
            
            return {
                "error": str(e),
                "execution_time": round(execution_time, 2),
                "playlist": [],
                "explanation": "Failed to curate playlist due to an error."
            }
    
    def _parse_agent_output(
        self,
        final_answer: str,
        intermediate_steps: List[tuple]
    ) -> Dict[str, Any]:
        """
        Parse agent output to extract playlist and explanation.
        """
        result = {
            "playlist": [],
            "explanation": "",
            "diversity_metrics": {},
            "intermediate_steps_count": len(intermediate_steps)
        }
        
        try:
            # Look through intermediate steps for tool outputs
            for step in intermediate_steps:
                action, observation = step
                tool_name = action.tool
                
                if tool_name == "optimize_diversity":
                    # Extract playlist from diversity optimization
                    try:
                        diversity_result = json.loads(observation)
                        result['playlist'] = diversity_result.get('playlist', [])
                        result['diversity_metrics'] = diversity_result.get('diversity_metrics', {})
                    except:
                        pass
                
                elif tool_name == "generate_explanation":
                    # Extract explanation
                    try:
                        explanation_result = json.loads(observation)
                        result['explanation'] = explanation_result.get('explanation', '')
                    except:
                        pass
            
            # If no explanation in steps, use final answer
            if not result['explanation']:
                result['explanation'] = final_answer
            
            logger.info(f"Parsed {len(result['playlist'])} tracks and explanation")
            
        except Exception as e:
            logger.error(f"Error parsing agent output: {e}")
        
        return result
    
    def _extract_strategy(self, intermediate_steps: List[tuple]) -> Dict[str, Any]:
        """
        Extract curation strategy from intermediate steps.
        """
        strategy = {
            "tools_used": [],
            "reasoning_steps": []
        }
        
        for step in intermediate_steps:
            action, observation = step
            strategy['tools_used'].append(action.tool)
            strategy['reasoning_steps'].append(action.log)
        
        return strategy


# Singleton instance
_curator_agent = None


def get_curator_agent() -> PlaylistCuratorAgent:
    """Get or create the Playlist Curator Agent singleton."""
    global _curator_agent
    if _curator_agent is None:
        _curator_agent = PlaylistCuratorAgent()
    return _curator_agent


def create_curator_agent() -> PlaylistCuratorAgent:
    """Create a new Playlist Curator Agent instance."""
    return PlaylistCuratorAgent()
