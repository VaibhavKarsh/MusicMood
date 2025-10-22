"""
UI Utilities for MusicMood Streamlit Frontend
Common components and helper functions
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime


def display_track_card(track: Dict[str, Any], index: int = 1):
    """
    Display a track card with metadata.
    
    Args:
        track: Track metadata dictionary
        index: Track number/position
    """
    with st.container():
        col1, col2, col3 = st.columns([0.5, 3, 1])
        
        with col1:
            st.markdown(f"**#{index}**")
        
        with col2:
            st.markdown(f"**{track.get('name', 'Unknown Track')}**")
            
            # Handle artist format (could be string or dict)
            artist = track.get('artist', 'Unknown Artist')
            if isinstance(artist, dict):
                artist = artist.get('name', 'Unknown Artist')
            elif isinstance(artist, list) and artist:
                artist = artist[0] if isinstance(artist[0], str) else artist[0].get('name', 'Unknown Artist')
            
            album = track.get('album', 'Unknown Album')
            if isinstance(album, dict):
                album = album.get('name', 'Unknown Album')
            
            st.caption(f"{artist} • {album}")
            
            # Audio features if available
            if track.get('audio_features'):
                features = track['audio_features']
                feat_col1, feat_col2, feat_col3 = st.columns(3)
                with feat_col1:
                    st.caption(f"⚡ Energy: {features.get('energy', 0):.0%}")
                with feat_col2:
                    st.caption(f"💃 Dance: {features.get('danceability', 0):.0%}")
                with feat_col3:
                    st.caption(f"😊 Valence: {features.get('valence', 0):.0%}")
        
        with col3:
            spotify_url = track.get('spotify_url', track.get('external_urls', {}).get('spotify'))
            if spotify_url:
                st.link_button("🎵 Play", spotify_url, use_container_width=True)
        
        st.divider()


def display_mood_data(mood_data: Dict[str, Any]):
    """
    Display mood analysis data.
    
    Args:
        mood_data: Mood analysis dictionary
    """
    st.markdown("### 🧠 Mood Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        primary_mood = mood_data.get('primary_mood', 'Unknown').capitalize()
        st.metric("Primary Mood", f"{primary_mood} 🎭")
    
    with col2:
        energy = mood_data.get('energy_level', 0)
        st.metric("Energy Level", f"{energy}/10 ⚡")
    
    with col3:
        intensity = mood_data.get('emotional_intensity', 0)
        st.metric("Intensity", f"{intensity}/10 🔥")
    
    # Mood tags
    mood_tags = mood_data.get('mood_tags', [])
    if mood_tags:
        st.markdown("**Detected Tags:**")
        tags_html = " ".join([f'<span style="background: #1DB954; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; margin: 0.2rem; display: inline-block;">{tag}</span>' for tag in mood_tags])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    # Context
    context = mood_data.get('context', 'general')
    if context != 'general':
        st.info(f"📍 Context: {context.capitalize()}")


def display_diversity_metrics(metrics: Dict[str, Any]):
    """
    Display diversity metrics.
    
    Args:
        metrics: Diversity metrics dictionary
    """
    if not metrics or not any(metrics.values()):
        return
    
    st.markdown("### 📊 Playlist Diversity")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Unique Artists", metrics.get('unique_artists', 0))
    
    with col2:
        tempo_mean = metrics.get('tempo_mean', 0)
        st.metric("Avg Tempo", f"{tempo_mean:.0f} BPM" if tempo_mean > 0 else "N/A")
    
    with col3:
        energy_mean = metrics.get('energy_mean', 0)
        st.metric("Avg Energy", f"{energy_mean:.0%}" if energy_mean > 0 else "N/A")
    
    with col4:
        diversity_score = metrics.get('diversity_score', 0)
        st.metric("Diversity Score", f"{diversity_score:.0f}/100" if diversity_score > 0 else "N/A")


def display_execution_times(times: Dict[str, Any], total: float):
    """
    Display execution time breakdown.
    
    Args:
        times: Execution times dictionary
        total: Total execution time
    """
    st.markdown("### ⏱️ Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        agent1_time = times.get('agent1_mood_understanding', 0)
        st.metric("Agent 1", f"{agent1_time:.1f}s", help="Mood Understanding Agent")
    
    with col2:
        agent2_time = times.get('agent2_music_discovery', 0)
        st.metric("Agent 2", f"{agent2_time:.1f}s", help="Music Discovery Agent")
    
    with col3:
        agent3_time = times.get('agent3_playlist_curator', 0)
        st.metric("Agent 3", f"{agent3_time:.1f}s" if agent3_time > 0 else "Premium", help="Playlist Curator Agent")
    
    with col4:
        st.metric("Total Time", f"{total:.1f}s", help="Total pipeline execution time")


def display_premium_message(message: str):
    """
    Display premium feature message.
    
    Args:
        message: Premium feature message
    """
    st.warning("⭐ **Premium Feature Required**")
    st.info(message)
    
    st.markdown("""
    ### Unlock Premium Features:
    - 🎯 Advanced AI playlist curation
    - 🎵 Audio analysis (tempo, energy, valence)
    - 🏆 Smart track ranking
    - 🌈 Diversity optimization
    - 💬 AI-generated explanations
    
    **Upgrade to Spotify Premium API access to unlock these features!**
    """)


def display_playlist_summary(
    playlist: List[Dict[str, Any]],
    mood_data: Dict[str, Any],
    created_at: Optional[datetime] = None
):
    """
    Display playlist summary card.
    
    Args:
        playlist: List of tracks
        mood_data: Mood analysis data
        created_at: Creation timestamp
    """
    mood = mood_data.get('primary_mood', 'unknown').capitalize()
    track_count = len(playlist)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%); 
                padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <h3 style="color: white; margin: 0;">{mood} Vibes Playlist 🎵</h3>
        <p style="color: white; opacity: 0.9; margin: 0.5rem 0;">
            {track_count} tracks perfectly matched to your mood
        </p>
        {f'<p style="color: white; opacity: 0.8; font-size: 0.9rem; margin: 0;">Created: {created_at.strftime("%B %d, %Y at %I:%M %p")}</p>' if created_at else ''}
    </div>
    """, unsafe_allow_html=True)


def display_loading_animation():
    """Display a custom loading animation"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 3rem; animation: pulse 1.5s ease-in-out infinite;">
            🎵
        </div>
        <h3>Generating your perfect playlist...</h3>
        <p style="color: #b3b3b3;">Our AI agents are working their magic ✨</p>
    </div>
    
    <style>
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
        }
    </style>
    """, unsafe_allow_html=True)


def format_duration(ms: int) -> str:
    """
    Format duration from milliseconds to MM:SS.
    
    Args:
        ms: Duration in milliseconds
        
    Returns:
        Formatted duration string
    """
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


def get_mood_emoji(mood: str) -> str:
    """
    Get emoji for a mood.
    
    Args:
        mood: Mood name
        
    Returns:
        Emoji character
    """
    mood_emojis = {
        'happy': '😊',
        'sad': '😢',
        'energetic': '⚡',
        'calm': '😌',
        'excited': '🤩',
        'anxious': '😰',
        'angry': '😠',
        'relaxed': '😎',
        'motivated': '💪',
        'focused': '🎯',
        'romantic': '💕',
        'nostalgic': '🌅',
    }
    
    return mood_emojis.get(mood.lower(), '🎭')


def display_error(error_message: str):
    """
    Display a user-friendly error message.
    
    Args:
        error_message: Error message to display
    """
    st.error(f"❌ **Oops! Something went wrong**")
    st.warning(error_message)
    
    with st.expander("🔍 Troubleshooting Tips"):
        st.markdown("""
        **Common Issues:**
        
        1. **API Connection Failed**
           - Make sure the FastAPI server is running
           - Check: `poetry run python -m app.main`
           - Default URL: http://localhost:8000
        
        2. **Request Timeout**
           - Agent 1 (local LLM) can take 60-120 seconds
           - Be patient during first request
           - Consider switching to cloud LLM API for faster response
        
        3. **Spotify API Issues**
           - Verify Spotify credentials in `.env`
           - Check if you're within API rate limits
           - Audio features require Premium API access
        
        **Need Help?** Check the logs or create an issue on GitHub.
        """)
