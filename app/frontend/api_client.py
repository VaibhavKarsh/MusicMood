"""
API Client for MusicMood Streamlit Frontend
Handles all communication with the FastAPI backend
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class MusicMoodAPIClient:
    """Client for interacting with MusicMood FastAPI backend"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the FastAPI backend
        """
        self.base_url = base_url or st.secrets.get("API_BASE_URL", "http://localhost:8000")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Health status information
            
        Raises:
            requests.RequestException: If request fails
        """
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Health check failed: {e}")
            raise
    
    def generate_playlist(
        self,
        user_input: str,
        user_id: str = "anonymous",
        desired_count: int = 30
    ) -> Dict[str, Any]:
        """
        Generate a playlist based on mood.
        
        Args:
            user_input: Natural language mood description
            user_id: User identifier
            desired_count: Number of tracks desired
            
        Returns:
            Playlist generation result
            
        Raises:
            requests.RequestException: If request fails
        """
        try:
            payload = {
                "user_input": user_input,
                "user_id": user_id,
                "desired_count": desired_count
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate-playlist",
                json=payload,
                timeout=180  # 3 minutes for Agent 1 (local LLM)
            )
            response.raise_for_status()
            return response.json()
            
        except requests.Timeout:
            raise Exception("Request timed out. The AI agents may be taking longer than expected.")
        except requests.RequestException as e:
            logger.error(f"Generate playlist failed: {e}")
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise Exception(f"API Error: {error_detail.get('detail', str(e))}")
                except:
                    raise Exception(f"API Error: {e.response.status_code} - {e.response.text}")
            raise
    
    def get_user_playlists(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get playlists for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of playlists to return
            offset: Number of playlists to skip
            
        Returns:
            User's playlists with metadata
            
        Raises:
            requests.RequestException: If request fails
        """
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            
            response = self.session.get(
                f"{self.base_url}/api/playlists/{user_id}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Get playlists failed: {e}")
            raise
    
    def submit_feedback(
        self,
        playlist_id: str,
        rating: int,
        feedback_text: Optional[str] = None,
        liked_tracks: Optional[List[str]] = None,
        disliked_tracks: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback for a playlist.
        
        Args:
            playlist_id: Playlist identifier
            rating: Rating from 1-5
            feedback_text: Optional text feedback
            liked_tracks: List of liked track IDs
            disliked_tracks: List of disliked track IDs
            
        Returns:
            Feedback submission confirmation
            
        Raises:
            requests.RequestException: If request fails
        """
        try:
            payload = {
                "playlist_id": playlist_id,
                "rating": rating,
                "feedback_text": feedback_text,
                "liked_tracks": liked_tracks or [],
                "disliked_tracks": disliked_tracks or []
            }
            
            response = self.session.post(
                f"{self.base_url}/api/feedback",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Submit feedback failed: {e}")
            raise
    
    def get_mood_history(
        self,
        user_id: str,
        limit: int = 30,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get mood history for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            
        Returns:
            User's mood history
            
        Raises:
            requests.RequestException: If request fails
        """
        try:
            params = {
                "limit": limit,
                "offset": offset
            }
            
            response = self.session.get(
                f"{self.base_url}/api/mood-history/{user_id}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Get mood history failed: {e}")
            raise


# Singleton instance
@st.cache_resource
def get_api_client() -> MusicMoodAPIClient:
    """
    Get cached API client instance.
    
    Returns:
        MusicMoodAPIClient instance
    """
    return MusicMoodAPIClient()
