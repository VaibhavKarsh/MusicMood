"""
My Playlists Page
View and manage saved playlists
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import get_api_client
from ui_utils import get_mood_emoji, display_error

# Initialize API client
api = get_api_client()

st.title("📚 My Playlists")
st.markdown("Browse your generated playlists and relive your musical moments!")

# Get user ID
user_id = st.session_state.get('user_id', 'anonymous')

# Pagination controls
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(f"**User:** {user_id}")

with col2:
    page_size = st.selectbox("Per page:", [10, 25, 50, 100], index=1)

with col3:
    if 'playlist_page' not in st.session_state:
        st.session_state.playlist_page = 0
    
    current_page = st.session_state.playlist_page

# Fetch playlists
try:
    with st.spinner("Loading your playlists..."):
        response = api.get_user_playlists(
            user_id=user_id,
            limit=page_size,
            offset=current_page * page_size
        )
    
    playlists = response.get('playlists', [])
    total = response.get('total', 0)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    # Display summary
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Playlists", total)
    
    with col2:
        if playlists:
            avg_rating = sum(p.get('feedback_score', 0) for p in playlists if p.get('feedback_score')) / len([p for p in playlists if p.get('feedback_score')]) if any(p.get('feedback_score') for p in playlists) else 0
            st.metric("Avg Rating", f"{'⭐' * int(avg_rating) if avg_rating > 0 else 'N/A'}")
        else:
            st.metric("Avg Rating", "N/A")
    
    with col3:
        if playlists:
            total_tracks = sum(p.get('track_count', 0) for p in playlists)
            st.metric("Total Tracks", total_tracks)
        else:
            st.metric("Total Tracks", 0)
    
    with col4:
        st.metric("Current Page", f"{current_page + 1} / {total_pages}")
    
    st.markdown("---")
    
    # Display playlists
    if not playlists:
        st.info("🎵 No playlists found. Generate your first playlist to get started!")
        
        if st.button("🚀 Generate Playlist", type="primary"):
            st.switch_page("pages/1_🎵_Generate_Playlist.py")
    
    else:
        # Search and filter
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search playlists", placeholder="Search by name or mood...")
        
        with col2:
            mood_filter = st.selectbox(
                "Filter by mood:",
                ["All"] + list(set(p.get('mood', 'unknown') for p in playlists))
            )
        
        # Filter playlists
        filtered_playlists = playlists
        
        if search_term:
            search_lower = search_term.lower()
            filtered_playlists = [
                p for p in filtered_playlists
                if search_lower in p.get('name', '').lower()
                or search_lower in p.get('mood', '').lower()
                or search_lower in p.get('description', '').lower()
            ]
        
        if mood_filter != "All":
            filtered_playlists = [p for p in filtered_playlists if p.get('mood') == mood_filter]
        
        if not filtered_playlists:
            st.warning("No playlists match your filters")
        else:
            st.caption(f"Showing {len(filtered_playlists)} playlist(s)")
            
            # Display each playlist
            for playlist in filtered_playlists:
                with st.container():
                    # Playlist card
                    mood = playlist.get('mood', 'unknown')
                    emoji = get_mood_emoji(mood)
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {emoji} {playlist.get('name', 'Untitled Playlist')}")
                        st.caption(playlist.get('description', 'No description')[:150] + "...")
                        
                        # Metadata
                        created = playlist.get('created_at')
                        if created:
                            if isinstance(created, str):
                                try:
                                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                                    st.caption(f"📅 Created: {created_dt.strftime('%B %d, %Y at %I:%M %p')}")
                                except:
                                    st.caption(f"📅 Created: {created}")
                            else:
                                st.caption(f"📅 Created: {created}")
                    
                    with col2:
                        st.markdown("**Details**")
                        st.caption(f"🎵 {playlist.get('track_count', 0)} tracks")
                        st.caption(f"🎭 Mood: {mood.capitalize()}")
                        
                        # Rating
                        rating = playlist.get('feedback_score')
                        if rating:
                            st.caption(f"⭐ Rating: {'⭐' * rating}")
                        else:
                            st.caption("⭐ Not rated")
                    
                    with col3:
                        st.markdown("**Actions**")
                        
                        if st.button("👁️ View", key=f"view_{playlist.get('id')}", use_container_width=True):
                            st.info("📝 Detailed playlist view coming soon!")
                        
                        if st.button("🗑️ Delete", key=f"delete_{playlist.get('id')}", use_container_width=True):
                            st.warning("🚧 Delete functionality coming soon!")
                    
                    st.divider()
    
    # Pagination
    if total_pages > 1:
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ First", disabled=current_page == 0):
                st.session_state.playlist_page = 0
                st.rerun()
        
        with col2:
            if st.button("◀️ Previous", disabled=current_page == 0):
                st.session_state.playlist_page = current_page - 1
                st.rerun()
        
        with col3:
            st.markdown(f"<div style='text-align: center; padding-top: 0.5rem;'>Page {current_page + 1} of {total_pages}</div>", unsafe_allow_html=True)
        
        with col4:
            if st.button("Next ▶️", disabled=current_page >= total_pages - 1):
                st.session_state.playlist_page = current_page + 1
                st.rerun()
        
        with col5:
            if st.button("Last ⏭️", disabled=current_page >= total_pages - 1):
                st.session_state.playlist_page = total_pages - 1
                st.rerun()

except Exception as e:
    display_error(str(e))

# Sidebar stats
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Playlist Stats")
    
    try:
        # Get recent playlists for stats
        stats_response = api.get_user_playlists(user_id=user_id, limit=100, offset=0)
        all_playlists = stats_response.get('playlists', [])
        
        if all_playlists:
            # Most common mood
            moods = [p.get('mood', 'unknown') for p in all_playlists]
            most_common_mood = max(set(moods), key=moods.count) if moods else 'N/A'
            
            st.metric("Most Common Mood", most_common_mood.capitalize())
            
            # Total tracks across all playlists
            total_tracks = sum(p.get('track_count', 0) for p in all_playlists)
            st.metric("Total Tracks Generated", total_tracks)
            
            # Rated playlists
            rated = len([p for p in all_playlists if p.get('feedback_score')])
            st.metric("Rated Playlists", f"{rated}/{len(all_playlists)}")
        else:
            st.info("No stats available yet")
    
    except:
        st.info("Unable to load stats")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #b3b3b3; font-size: 0.9rem;">
        <p>💾 Playlists are automatically saved when generated</p>
        <p>⭐ Rate your playlists to help improve recommendations</p>
    </div>
    """,
    unsafe_allow_html=True
)
