"""
Generate Playlist Page
Main playlist generation interface with full AI pipeline integration
"""

import streamlit as st
import sys
import os

# Add parent directory to path to import from app.frontend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import get_api_client
from ui_utils import (
    display_track_card,
    display_mood_data,
    display_diversity_metrics,
    display_execution_times,
    display_premium_message,
    display_playlist_summary,
    display_loading_animation,
    display_error
)

# Initialize API client
api = get_api_client()

# Page title
st.title("🎵 Generate Playlist")
st.markdown("Describe your mood and let our AI create the perfect playlist for you!")

# Mood input section
st.markdown("### 💭 How are you feeling?")

# Example prompts
with st.expander("� Need inspiration? Try these examples:"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Energy & Motivation:**
        - "I'm feeling energetic and ready to workout!"
        - "Need motivation to finish this project"
        - "Pump me up for the game!"
        
        **Relaxation:**
        - "I want to relax after a long day"
        - "Need calm music for meditation"
        - "Help me wind down for sleep"
        """)
    
    with col2:
        st.markdown("""
        **Work & Focus:**
        - "I need to focus on studying"
        - "Give me productive coding music"
        - "Background music for work"
        
        **Mood & Emotion:**
        - "I'm feeling happy and optimistic!"
        - "Need something uplifting"
        - "Feeling nostalgic today"
        """)

# Mood input
user_input = st.text_area(
    "Describe your mood in your own words:",
    placeholder="e.g., I'm feeling happy and energetic, ready to conquer the day!",
    height=100,
    help="Be specific! The more details you provide, the better the playlist.",
    key="mood_input"
)

# Options
col1, col2 = st.columns([2, 1])

with col1:
    desired_count = st.slider(
        "Number of tracks:",
        min_value=5,
        max_value=50,
        value=30,
        step=5,
        help="How many tracks do you want in your playlist?"
    )

with col2:
    st.markdown("**User ID:**")
    user_id = st.session_state.get('user_id', 'anonymous')
    st.text(user_id)

# Generate button
generate_button = st.button(
    "🚀 Generate Playlist",
    type="primary",
    use_container_width=True,
    disabled=not user_input or len(user_input.strip()) < 3
)

if not user_input or len(user_input.strip()) < 3:
    st.info("👆 Enter your mood description above to generate a playlist")

# Handle playlist generation
if generate_button:
    # Clear previous results
    if 'playlist_result' in st.session_state:
        del st.session_state['playlist_result']
    
    # Show loading state
    with st.spinner(""):
        display_loading_animation()
        
        # Progress indicator
        progress_container = st.container()
        with progress_container:
            st.markdown("### 🤖 AI Pipeline Progress")
            
            agent1_status = st.empty()
            agent2_status = st.empty()
            agent3_status = st.empty()
            
            agent1_status.info("🧠 **Agent 1:** Understanding your mood...")
            agent2_status.info("🎵 **Agent 2:** Waiting...")
            agent3_status.info("✨ **Agent 3:** Waiting...")
        
        try:
            # Call API
            result = api.generate_playlist(
                user_input=user_input,
                user_id=user_id,
                desired_count=desired_count
            )
            
            # Update progress
            agent1_status.success("✅ **Agent 1:** Mood understood!")
            agent2_status.info("🎵 **Agent 2:** Discovering music...")
            
            # Small delay for UX
            import time
            time.sleep(0.5)
            
            agent2_status.success("✅ **Agent 2:** Music discovered!")
            
            # Check if premium required
            if result.get('premium_feature_required'):
                agent3_status.warning("⭐ **Agent 3:** Premium feature (not executed)")
            else:
                agent3_status.info("✨ **Agent 3:** Curating playlist...")
                time.sleep(0.5)
                agent3_status.success("✅ **Agent 3:** Playlist curated!")
            
            # Store result in session state
            st.session_state['playlist_result'] = result
            
            # Clear progress and show results
            progress_container.empty()
            
        except Exception as e:
            progress_container.empty()
            display_error(str(e))
            st.stop()

# Display results if available
if 'playlist_result' in st.session_state:
    result = st.session_state['playlist_result']
    
    st.markdown("---")
    st.markdown("## 🎉 Your Playlist is Ready!")
    
    # Check if it's a premium-gated result
    if result.get('premium_feature_required'):
        st.warning("⚠️ **Limited Result - Free Tier**")
        
        # Show what was accomplished
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Mood Analyzed", "✅", help="Agent 1 completed")
        with col2:
            candidates = result.get('candidate_tracks_count', 0)
            st.metric("Tracks Found", f"{candidates}", help="Agent 2 completed")
        with col3:
            st.metric("Curation", "⭐ Premium", help="Agent 3 requires upgrade")
        
        st.markdown("---")
        
        # Display mood analysis
        mood_data = result.get('mood_data', {})
        if mood_data:
            display_mood_data(mood_data)
        
        st.markdown("---")
        
        # Display execution times
        execution_times = result.get('execution_times', {})
        total_time = result.get('total_execution_time', 0)
        if execution_times:
            display_execution_times(execution_times, total_time)
        
        st.markdown("---")
        
        # Show premium message
        premium_message = result.get('premium_feature_message', '')
        if premium_message:
            display_premium_message(premium_message)
        
        # Additional info
        st.markdown("### 🎵 What You're Missing")
        st.markdown(f"""
        We found **{candidates} candidate tracks** that match your mood, but the advanced 
        AI curation features require Spotify Premium API access:
        
        - 🎯 **Smart Ranking**: Tracks ranked by mood relevance
        - 🌈 **Diversity Optimization**: Balanced artist and tempo distribution
        - 💬 **AI Explanation**: Detailed reasoning for each selection
        - 📊 **Audio Analysis**: Tempo, energy, and valence matching
        
        With Premium, you'd get the **top {desired_count} perfectly curated tracks**!
        """)
    
    else:
        # Success! Show full playlist
        playlist = result.get('playlist', [])
        mood_data = result.get('mood_data', {})
        diversity_metrics = result.get('diversity_metrics', {})
        execution_times = result.get('execution_times', {})
        total_time = result.get('total_execution_time', 0)
        explanation = result.get('explanation', '')
        
        # Playlist summary
        display_playlist_summary(playlist, mood_data)
        
        # Download/Export options
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📥 Export to Spotify", use_container_width=True, disabled=True, help="Coming soon!")
        with col2:
            st.button("� Copy Track List", use_container_width=True, disabled=True, help="Coming soon!")
        with col3:
            st.button("⭐ Save Playlist", use_container_width=True, disabled=True, help="Coming soon!")
        
        st.markdown("---")
        
        # Mood analysis
        if mood_data:
            display_mood_data(mood_data)
        
        st.markdown("---")
        
        # AI Explanation
        if explanation:
            st.markdown("### 💬 AI Curator's Explanation")
            st.info(explanation)
            st.markdown("---")
        
        # Diversity metrics
        if diversity_metrics:
            display_diversity_metrics(diversity_metrics)
            st.markdown("---")
        
        # Performance metrics
        if execution_times:
            display_execution_times(execution_times, total_time)
            st.markdown("---")
        
        # Playlist tracks
        st.markdown(f"### 🎵 Your Playlist ({len(playlist)} tracks)")
        
        if playlist:
            # Search and filter
            search_term = st.text_input("🔍 Search tracks", placeholder="Search by title, artist, or album...")
            
            # Filter playlist
            filtered_playlist = playlist
            if search_term:
                search_lower = search_term.lower()
                filtered_playlist = [
                    track for track in playlist
                    if search_lower in track.get('name', '').lower()
                    or search_lower in str(track.get('artist', '')).lower()
                    or search_lower in str(track.get('album', '')).lower()
                ]
            
            if not filtered_playlist:
                st.warning(f"No tracks found matching '{search_term}'")
            else:
                st.caption(f"Showing {len(filtered_playlist)} of {len(playlist)} tracks")
                
                # Display tracks
                for idx, track in enumerate(filtered_playlist, 1):
                    display_track_card(track, idx)
        else:
            st.info("No tracks in playlist")
        
        st.markdown("---")
        
        # Feedback section
        st.markdown("### 📝 Rate This Playlist")
        st.markdown("Help us improve! How would you rate this playlist?")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            rating = st.select_slider(
                "Rating:",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: "⭐" * x,
                key="playlist_rating"
            )
        
        with col2:
            feedback_text = st.text_area(
                "Feedback (optional):",
                placeholder="Tell us what you liked or what could be improved...",
                height=100,
                key="feedback_text"
            )
        
        if st.button("📤 Submit Feedback", type="secondary"):
            st.success("✅ Thank you for your feedback! (Feature in development)")
            st.info("💡 Feedback submission to API will be implemented in the next phase.")

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    if 'playlist_result' in st.session_state:
        result = st.session_state['playlist_result']
        
        # Stats
        st.metric("Mood", result.get('mood_data', {}).get('primary_mood', 'N/A').capitalize())
        st.metric("Tracks", len(result.get('playlist', [])))
        st.metric("Generation Time", f"{result.get('total_execution_time', 0):.1f}s")
        
        if result.get('premium_feature_required'):
            st.warning("⭐ Premium Required")
        else:
            st.success("✅ Full Playlist")
    else:
        st.info("Generate a playlist to see stats here!")

# Tips
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    **For best results:**
    - Be specific about your mood
    - Mention activities (workout, study, relax)
    - Include energy level descriptors
    - Describe the vibe you want
    
    **Examples:**
    - "Energetic workout music"
    - "Calm focus for coding"
    - "Happy morning vibes"
    """)

# Footer note
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #b3b3b3; font-size: 0.9rem;">
        <p>💡 First generation may take 60-120 seconds due to local LLM processing</p>
        <p>⚡ Subsequent requests will be faster</p>
    </div>
    """,
    unsafe_allow_html=True
)
