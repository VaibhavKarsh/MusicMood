"""
Mood analysis tools for the Mood Understanding Agent.
Uses LLM to parse and structure user mood input.
"""

import json
import logging
from typing import Dict, Any, Optional

from langchain_ollama import OllamaLLM
from langchain.tools import Tool

from app.config.settings import settings

logger = logging.getLogger(__name__)


# Initialize Ollama LLM
llm = OllamaLLM(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=settings.OLLAMA_TEMPERATURE,
    num_predict=settings.OLLAMA_MAX_TOKENS,
)


def parse_mood_with_llm(mood_text: str) -> str:
    """
    Parse user mood text into structured mood data using LLM.

    Extracts:
    - primary_mood: Main emotional state (happy, sad, energetic, calm, focused, stressed, anxious, etc.)
    - energy_level: Energy level on 1-10 scale
    - emotional_intensity: Intensity of emotion on 1-10 scale
    - context: Situation context (work, gym, sleep, party, study, commute, relaxing, etc.)
    - mood_tags: List of additional mood descriptors

    Args:
        mood_text: User's mood description

    Returns:
        JSON string with structured mood data

    Example:
        Input: "I'm feeling super energized and ready to work out!"
        Output: {
            "primary_mood": "energetic",
            "energy_level": 9,
            "emotional_intensity": 8,
            "context": "gym",
            "mood_tags": ["motivated", "excited", "active"]
        }
    """

    logger.info(f"Parsing mood text: {mood_text[:100]}...")

    prompt = f"""You are a mood analysis expert. Analyze the following mood description and extract structured data.

User's mood: "{mood_text}"

Extract the following information and return ONLY a valid JSON object (no other text):

{{
    "primary_mood": "<one of: happy, sad, energetic, calm, focused, stressed, anxious, melancholic, excited, relaxed, romantic, angry, peaceful>",
    "energy_level": <number 1-10, where 1=very low energy, 10=very high energy>,
    "emotional_intensity": <number 1-10, where 1=mild feeling, 10=very intense feeling>,
    "context": "<one of: work, gym, sleep, party, study, commute, relaxing, social, alone, morning, evening, weekend, or 'general'>",
    "mood_tags": [<list of 2-5 additional mood descriptors like "motivated", "tired", "optimistic", etc.>]
}}

Guidelines:
- Choose the primary_mood that best matches the overall feeling
- energy_level should reflect physical/mental energy (not just emotional state)
- emotional_intensity reflects how strongly they feel this emotion
- context should match the situation if mentioned, otherwise use "general"
- mood_tags should be specific adjectives describing the mood

Return only the JSON object, nothing else."""

    try:
        response = llm.invoke(prompt)

        # Try to extract JSON from response
        # Sometimes LLMs add extra text, so we need to find the JSON part
        response = response.strip()

        # Find JSON object in response
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]

            # Validate JSON
            parsed = json.loads(json_str)

            # Validate structure
            required_fields = ['primary_mood', 'energy_level', 'emotional_intensity', 'context', 'mood_tags']
            for field in required_fields:
                if field not in parsed:
                    raise ValueError(f"Missing required field: {field}")

            # Validate ranges
            if not (1 <= parsed['energy_level'] <= 10):
                parsed['energy_level'] = max(1, min(10, parsed['energy_level']))

            if not (1 <= parsed['emotional_intensity'] <= 10):
                parsed['emotional_intensity'] = max(1, min(10, parsed['emotional_intensity']))

            logger.info(f"Successfully parsed mood: {parsed['primary_mood']}, energy: {parsed['energy_level']}")
            return json.dumps(parsed)

        else:
            raise ValueError("No JSON object found in LLM response")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM response: {e}")
        logger.debug(f"LLM response was: {response}")

        # Return fallback mood data
        fallback = {
            "primary_mood": "calm",
            "energy_level": 5,
            "emotional_intensity": 5,
            "context": "general",
            "mood_tags": ["neutral"],
            "error": "Failed to parse mood, using fallback"
        }
        return json.dumps(fallback)

    except Exception as e:
        logger.error(f"Error parsing mood: {e}")

        # Return error with fallback
        fallback = {
            "primary_mood": "calm",
            "energy_level": 5,
            "emotional_intensity": 5,
            "context": "general",
            "mood_tags": ["neutral"],
            "error": str(e)
        }
        return json.dumps(fallback)


# Create LangChain Tool
parse_mood_tool = Tool(
    name="parse_mood_with_llm",
    func=parse_mood_with_llm,
    description="""
    Parse user's mood description into structured data.
    Input: A text description of how the user is feeling.
    Output: JSON with primary_mood, energy_level (1-10), emotional_intensity (1-10), context, and mood_tags.
    Use this tool when you need to understand and structure the user's emotional state from their text input.
    """
)


def get_mood_description(mood_data: Dict[str, Any]) -> str:
    """
    Generate a natural language description from structured mood data.

    Args:
        mood_data: Dictionary with mood information

    Returns:
        Natural language description of the mood
    """

    primary_mood = mood_data.get('primary_mood', 'neutral')
    energy_level = mood_data.get('energy_level', 5)
    emotional_intensity = mood_data.get('emotional_intensity', 5)
    context = mood_data.get('context', 'general')
    mood_tags = mood_data.get('mood_tags', [])

    # Energy descriptors
    if energy_level >= 8:
        energy_desc = "very high energy"
    elif energy_level >= 6:
        energy_desc = "good energy"
    elif energy_level >= 4:
        energy_desc = "moderate energy"
    else:
        energy_desc = "low energy"

    # Intensity descriptors
    if emotional_intensity >= 8:
        intensity_desc = "very intense"
    elif emotional_intensity >= 6:
        intensity_desc = "strong"
    elif emotional_intensity >= 4:
        intensity_desc = "moderate"
    else:
        intensity_desc = "mild"

    description = f"The user feels {primary_mood} ({intensity_desc}) with {energy_desc}"

    if context and context != "general":
        description += f" in a {context} context"

    if mood_tags:
        tags_str = ", ".join(mood_tags[:3])  # Show first 3 tags
        description += f". Additional descriptors: {tags_str}"

    return description


def get_user_context(user_id: Optional[str] = None) -> str:
    """
    Get user context information (placeholder for future user profile features).

    Args:
        user_id: Optional user ID to retrieve context for

    Returns:
        JSON string with user context data
    """
    # Placeholder implementation - will be enhanced in future phases
    context = {
        "user_id": user_id or "anonymous",
        "preferences": {
            "favorite_genres": [],
            "preferred_energy_level": 5,
            "listening_history": []
        },
        "note": "User context feature is a placeholder. Will be implemented in future phases."
    }

    return json.dumps(context)


# Create user context tool
user_context_tool = Tool(
    name="get_user_context",
    func=get_user_context,
    description="""
    Get user context and preferences (placeholder).
    Input: Optional user_id string
    Output: JSON with user preferences and listening history.
    This tool will be enhanced in future phases with actual user data.
    """
)
