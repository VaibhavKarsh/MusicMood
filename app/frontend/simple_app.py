"""
MusicMood - Simple Single Page App
"""
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="MusicMood", page_icon="🎵", layout="wide")

# Simple CSS
st.markdown("""
<style>
    .stApp { background: #1a1a2e; color: #eee; }
    h1, h2, h3 { color: #ffd700; }
    .stButton>button { background: #6d28d9; color: #ffd700; border: 1px solid #ffd700; }
</style>
""", unsafe_allow_html=True)

# API Config
API_BASE = "http://localhost:8000"

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "test_user"
if 'view' not in st.session_state:
    st.session_state.view = "generate"
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Title
st.title("🎵 MusicMood")
st.markdown("AI-Powered Playlist Generator")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.session_state.user_id = st.text_input("User ID:", st.session_state.user_id, key="user_input")
    
    st.markdown("---")
    
    st.header("Navigation")
    if st.button("🎵 Generate", use_container_width=True, key="nav_generate"):
        st.session_state.view = "generate"
        st.rerun()
    if st.button("📚 Playlists", use_container_width=True, key="nav_playlists"):
        st.session_state.view = "playlists"
        st.rerun()
    if st.button("📊 History", use_container_width=True, key="nav_history"):
        st.session_state.view = "history"
        st.rerun()
    
    st.markdown("---")
    
    # API Status
    try:
        resp = requests.get(f"{API_BASE}/api/health", timeout=2)
        st.success("✅ API Online")
    except:
        st.error("❌ API Offline")

# Main content area
st.markdown("---")

# View: Generate Playlist
if st.session_state.view == "generate":
    st.header("Generate Playlist")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        mood = st.text_area(
            "Describe your mood:",
            placeholder="I'm feeling energetic and happy!",
            height=100,
            key="mood_input"
        )
    
    with col2:
        count = st.number_input("Tracks:", min_value=5, max_value=50, value=20, key="track_count")
        st.write(f"User: {st.session_state.user_id}")
    
    if st.button("Generate Playlist", type="primary", use_container_width=True, key="generate_btn"):
        if not mood or len(mood.strip()) < 3:
            st.warning("Please enter a mood description")
        else:
            with st.spinner("Generating playlist..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/api/generate",
                        json={
                            "user_input": mood,
                            "user_id": st.session_state.user_id,
                            "desired_count": count
                        },
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.last_result = result
                        st.success(f"✅ Generated {len(result.get('tracks', []))} tracks!")
                        
                        # Show results
                        if result.get('mood_data'):
                            with st.expander("Mood Analysis", expanded=True):
                                mood_data = result['mood_data']
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Primary Mood", mood_data.get('primary_mood', 'N/A'))
                                col2.metric("Energy", mood_data.get('energy_level', 0))
                                col3.metric("Intensity", mood_data.get('emotional_intensity', 0))
                        
                        # Show tracks
                        if result.get('tracks'):
                            st.markdown("### 🎵 Tracks")
                            for idx, track in enumerate(result['tracks'][:10], 1):
                                with st.expander(f"{idx}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}"):
                                    col1, col2 = st.columns(2)
                                    col1.write(f"**Album:** {track.get('album', 'N/A')}")
                                    col2.write(f"**Popularity:** {track.get('popularity', 0)}")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("Request timed out. API may be slow.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# View: My Playlists
elif st.session_state.view == "playlists":
    st.header("My Playlists")
    
    limit = st.selectbox("Items per page:", [10, 25, 50], key="playlist_limit")
    
    if st.button("Load Playlists", type="primary", key="load_playlists_btn"):
        with st.spinner("Loading..."):
            try:
                response = requests.get(
                    f"{API_BASE}/api/playlists/{st.session_state.user_id}",
                    params={"limit": limit, "offset": 0},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    playlists = data.get('playlists', [])
                    
                    if playlists:
                        st.success(f"Found {data.get('total', 0)} playlists")
                        
                        for idx, pl in enumerate(playlists, 1):
                            with st.expander(f"Playlist {idx} - {pl.get('primary_mood', 'Unknown')}"):
                                col1, col2 = st.columns(2)
                                col1.write(f"**Tracks:** {pl.get('track_count', 0)}")
                                col2.write(f"**Date:** {pl.get('created_at', 'N/A')[:10]}")
                                
                                if st.button(f"View Details", key=f"view_pl_{idx}"):
                                    st.info(f"Playlist ID: {pl.get('id', 'N/A')}")
                    else:
                        st.info("No playlists found")
                else:
                    st.error(f"Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# View: Mood History
elif st.session_state.view == "history":
    st.header("Mood History")
    
    limit = st.selectbox("Items to load:", [20, 50, 100], key="history_limit")
    
    if st.button("Load History", type="primary", key="load_history_btn"):
        with st.spinner("Loading..."):
            try:
                response = requests.get(
                    f"{API_BASE}/api/mood-history/{st.session_state.user_id}",
                    params={"limit": limit, "offset": 0},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get('entries', [])
                    
                    if entries:
                        st.success(f"Found {data.get('total', 0)} entries")
                        
                        # Stats
                        moods = [e.get('mood_data', {}).get('primary_mood', 'unknown') for e in entries]
                        from collections import Counter
                        mood_counts = Counter(moods)
                        
                        st.markdown("### 📊 Statistics")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Entries", len(entries))
                        col2.metric("Unique Moods", len(mood_counts))
                        col3.metric("Most Common", mood_counts.most_common(1)[0][0] if mood_counts else "N/A")
                        
                        st.markdown("---")
                        
                        # List entries
                        for idx, entry in enumerate(entries[:20], 1):
                            mood_data = entry.get('mood_data', {})
                            with st.expander(f"{idx}. {mood_data.get('primary_mood', 'Unknown')} - {entry.get('created_at', 'N/A')[:10]}"):
                                col1, col2 = st.columns(2)
                                col1.write(f"**Energy:** {mood_data.get('energy_level', 0)}")
                                col2.write(f"**Intensity:** {mood_data.get('emotional_intensity', 0)}")
                    else:
                        st.info("No history found")
                else:
                    st.error(f"Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>MusicMood © 2025</p>", unsafe_allow_html=True)
