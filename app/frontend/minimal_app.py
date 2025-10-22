"""
MusicMood - Complete Professional UI Overhaul
"""
import streamlit as st
import requests
import os
from datetime import datetime
from collections import Counter

st.set_page_config(
    page_title="MusicMood", 
    page_icon="🎵", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PROFESSIONAL COMPLETE REDESIGN CSS
st.markdown("""
<style>
    /* ============ BASE STYLES ============ */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        background: #121212;
        color: #e0e0e0;
    }
    
    /* Hide sidebar and related elements */
    [data-testid="stSidebar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* ============ MAIN CONTAINER ============ */
    .stApp {
        background: #121212;
    }
    
    .block-container {
        padding: 3rem 2rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    
    @media (max-width: 768px) {
        .block-container {
            padding: 2rem 1rem !important;
        }
    }
    
    /* ============ TYPOGRAPHY ============ */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    h1 {
        font-size: 3.2rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    h2 {
        font-size: 1.8rem;
        color: #ffffff;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #2a2a2a;
        padding-bottom: 0.75rem;
    }
    
    h3 {
        font-size: 1.3rem;
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    p {
        color: #b0b0b0;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }
    
    /* ============ SUBTITLE ============ */
    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 1.1rem;
        letter-spacing: 1px;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* ============ TABS STYLING ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #1e1e1e;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
        border: 1px solid #2a2a2a;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888888;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        cursor: pointer;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: #252525;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2a2a2a !important;
        color: #ffffff !important;
        border-bottom: 3px solid #1db954 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* ============ BUTTONS ============ */
    .stButton > button {
        background: #1db954;
        color: #ffffff;
        border: none;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.5px;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    .stButton > button:hover {
        background: #1ed760;
        box-shadow: 0 4px 12px rgba(29, 185, 84, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ============ INPUT FIELDS ============ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1db954 !important;
        box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.2) !important;
        background: #252525 !important;
    }
    
    .stTextArea > div > div > textarea {
        min-height: 120px !important;
    }
    
    /* ============ LABELS ============ */
    .stTextInput > label,
    .stTextArea > label,
    .stNumberInput > label,
    .stSelectbox > label {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.6rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ============ COLUMNS & LAYOUT ============ */
    [data-testid="column"] {
        padding: 1rem 0.5rem !important;
    }
    
    .row-widget {
        gap: 1.5rem !important;
        margin-bottom: 1.5rem;
    }
    
    /* ============ EXPANDERS (CARDS) ============ */
    .stExpander {
        background: #1e1e1e;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        margin-bottom: 1.2rem;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    
    .stExpander:hover {
        background: #252525;
        border-color: #333333;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .stExpander > details > summary {
        padding: 1.2rem;
        cursor: pointer;
        font-weight: 600;
        color: #ffffff;
        user-select: none;
    }
    
    .stExpander > details > summary:hover {
        background: #252525;
    }
    
    .stExpander > details {
        padding: 0;
    }
    
    .stExpander > details > div {
        padding: 1.2rem;
        padding-top: 0;
        border-top: 1px solid #2a2a2a;
    }
    
    /* ============ METRICS ============ */
    [data-testid="stMetricValue"] {
        color: #1db954;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888;
        font-size: 0.95rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* ============ ALERTS & MESSAGES ============ */
    .stSuccess, .stError, .stInfo, .stWarning {
        background: #1e1e1e !important;
        border-radius: 8px !important;
        padding: 1.2rem !important;
        margin: 1.5rem 0 !important;
        border-left: 4px solid;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .stSuccess {
        border-left-color: #1db954 !important;
        background: rgba(29, 185, 84, 0.1) !important;
    }
    
    .stError {
        border-left-color: #e22134 !important;
        background: rgba(226, 33, 52, 0.1) !important;
    }
    
    .stInfo {
        border-left-color: #1e90ff !important;
        background: rgba(30, 144, 255, 0.1) !important;
    }
    
    .stWarning {
        border-left-color: #ffa500 !important;
        background: rgba(255, 165, 0, 0.1) !important;
    }
    
    .stSuccess > div, .stError > div, .stInfo > div, .stWarning > div {
        color: #e0e0e0 !important;
    }
    
    /* ============ DIVIDER ============ */
    hr {
        margin: 2rem 0 !important;
        border: 0;
        border-top: 1px solid #2a2a2a;
    }
    
    /* ============ FOOTER ============ */
    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #2a2a2a;
        letter-spacing: 1px;
    }
    
    /* ============ MARKDOWN TEXT ============ */
    .stMarkdown p {
        margin-bottom: 0.5rem;
    }
    
    /* ============ SPINNER ============ */
    .stSpinner > div {
        border-color: rgba(29, 185, 84, 0.3);
        border-top-color: #1db954 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Config - support both Docker and local development
# Read from environment variable (set in docker-compose.yml or locally)
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8001")

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user_demo"

# ============ HEADER ============
st.markdown("""
<div style="text-align: center; margin-bottom: 0;">
    <h1>🎵 MusicMood</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
    AI-Powered Playlist Generator
</div>
""", unsafe_allow_html=True)

# ============ TABS ============
tab1, tab2, tab3 = st.tabs(["🎵 Generate", "📚 Playlists", "📊 History"])

# ============ TAB 1: GENERATE PLAYLIST ============
with tab1:
    st.markdown("## Create Your Playlist")
    
    # Two-column layout for inputs
    col1, col2 = st.columns([1, 1])
    
    with col1:
        user_id = st.text_input(
            "User ID",
            value=st.session_state.user_id,
            placeholder="e.g., john_doe",
            key="user_id_input",
            help="Enter a unique identifier for your account"
        )
        st.session_state.user_id = user_id
    
    with col2:
        count_input = st.text_input(
            "Number of Tracks",
            value="20",
            placeholder="e.g., 20",
            key="track_count_input",
            help="Enter a number between 5 and 50"
        )
        
        # Convert to integer with validation
        try:
            count = int(count_input) if count_input else 20
        except ValueError:
            count = 20
            st.warning("⚠️ Invalid number, using default: 20")
    
    # Mood input (full width)
    mood = st.text_area(
        "Describe Your Mood",
        placeholder="e.g., I'm feeling energetic and ready to workout! I love fast-paced music with heavy bass.",
        key="mood_input",
        height=120,
        help="Tell us how you're feeling or what vibe you want"
    )
    
    st.markdown("")
    
    # Generate button with validation
    if st.button("🚀 Generate Playlist", type="primary", key="generate_btn", use_container_width=True):
        # Validation
        validation_errors = []
        
        if not user_id or len(user_id.strip()) == 0:
            validation_errors.append("⚠️ User ID is required")
        elif len(user_id.strip()) < 3:
            validation_errors.append("⚠️ User ID must be at least 3 characters")
        elif len(user_id.strip()) > 50:
            validation_errors.append("⚠️ User ID must be less than 50 characters")
        
        if not mood or len(mood.strip()) < 3:
            validation_errors.append("⚠️ Please enter a mood description (at least 3 characters)")
        elif len(mood.strip()) > 500:
            validation_errors.append("⚠️ Mood description is too long (max 500 characters)")
        
        if count < 5 or count > 50:
            validation_errors.append("⚠️ Number of tracks must be between 5 and 50")
        
        if validation_errors:
            for error in validation_errors:
                st.warning(error)
        else:
            with st.spinner("🎵 Generating your perfect playlist..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/api/generate-playlist",
                        json={
                            "user_input": mood.strip(),
                            "user_id": user_id.strip(),
                            "desired_count": count
                        },
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success(f"✅ Successfully generated {len(result.get('tracks', []))} tracks!")
                        
                        # Mood Analysis Section
                        if result.get('mood_data'):
                            st.markdown("### 🎭 Mood Analysis")
                            mood_data = result['mood_data']
                            
                            metric_col1, metric_col2, metric_col3 = st.columns(3)
                            with metric_col1:
                                st.metric("Primary Mood", mood_data.get('primary_mood', 'N/A').title())
                            with metric_col2:
                                st.metric("Energy Level", f"{mood_data.get('energy_level', 0)}/10")
                            with metric_col3:
                                st.metric("Intensity", f"{mood_data.get('emotional_intensity', 0)}/10")
                        
                        # Tracks Section
                        if result.get('tracks'):
                            st.markdown("### 🎵 Your Playlist")
                            st.markdown(f"*{len(result['tracks'])} tracks to match your mood*")
                            
                            for idx, track in enumerate(result['tracks'], 1):
                                track_name = track.get('name', 'Unknown')
                                artist_name = track.get('artist', 'Unknown')
                                
                                with st.expander(f"**{idx}.** {track_name} — {artist_name}"):
                                    col1, col2 = st.columns([1, 1])
                                    
                                    with col1:
                                        st.write(f"**Album:** {track.get('album', 'N/A')}")
                                        st.write(f"**Popularity:** {track.get('popularity', 0)}/100")
                                        st.write(f"**Year:** {track.get('year', 'N/A')}")
                                    
                                    with col2:
                                        if track.get('spotify_url'):
                                            st.markdown(f"[🎵 Listen on Spotify]({track['spotify_url']})")
                                        if track.get('preview_url'):
                                            st.audio(track.get('preview_url'), format="audio/mp3")
                        
                        # Execution Time
                        if result.get('total_execution_time'):
                            st.info(f"⏱️ Generated in {result['total_execution_time']:.2f} seconds")
                            
                    elif response.status_code == 404:
                        st.error("❌ **404 ERROR** - API endpoint not found. Backend is running but endpoint '/api/generate-playlist' doesn't exist!")
                    else:
                        st.error(f"❌ Error {response.status_code}: Unable to generate playlist")
                        
                except requests.exceptions.ConnectionError:
                    st.error("""
❌ **Backend API is not running**

Please start the backend server:
```bash
uvicorn app.backend.main:app --reload
```
                    """)
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. The API is taking too long to respond.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============ TAB 2: SAVED PLAYLISTS ============
with tab2:
    st.markdown("## Your Saved Playlists")
    
    st.write(f"**User ID:** `{st.session_state.user_id}`")
    
    st.markdown("")
    
    if st.button("📥 Load Playlists", type="primary", key="load_playlists_btn", use_container_width=True):
        with st.spinner("Loading your playlists..."):
            try:
                response = requests.get(
                    f"{API_BASE}/api/playlists/{st.session_state.user_id}",
                    params={"limit": 25, "offset": 0},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    playlists = data.get('playlists', [])
                    
                    if playlists:
                        st.success(f"✅ Found {data.get('total_count', 0)} saved playlists")
                        
                        for idx, pl in enumerate(playlists, 1):
                            mood = pl.get('mood', 'Unknown').title()
                            tracks = pl.get('track_count', 0)
                            date = pl.get('created_at', 'N/A')[:10]
                            
                            with st.expander(f"**{idx}.** {mood} — {tracks} tracks — {date}"):
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.write(f"**Playlist ID:** `{pl.get('id', 'N/A')}`")
                                    st.write(f"**Created:** {date}")
                                
                                with col2:
                                    st.write(f"**Total Tracks:** {tracks}")
                                    st.write(f"**Mood:** {mood}")
                                
                                # Show explanation
                                explanation = pl.get('explanation', '')
                                if explanation:
                                    st.markdown("**Description:**")
                                    st.info(explanation)
                                
                                # Show track list
                                track_list = pl.get('tracks', [])
                                if track_list:
                                    st.markdown("---")
                                    st.markdown("**🎵 Track List:**")
                                    for track_idx, track in enumerate(track_list, 1):
                                        track_name = track.get('name', 'Unknown')
                                        artist_name = track.get('artist', 'Unknown')
                                        album_name = track.get('album', 'Unknown')
                                        
                                        st.markdown(f"""
                                        **{track_idx}.** {track_name}  
                                        *Artist:* {artist_name} | *Album:* {album_name}
                                        """)
                                else:
                                    st.write("*No track details available*")
                    else:
                        st.info("📝 No playlists found. Generate your first playlist in the **Generate** tab!")
                        
                elif response.status_code == 404:
                    st.warning("⚠️ No playlists found for this user. Start by generating your first playlist!")
                else:
                    st.error(f"❌ Error {response.status_code}: Unable to load playlists")
                    
            except requests.exceptions.ConnectionError:
                st.error("""
❌ **Backend API is not running**

Please start the backend server:
```bash
uvicorn app.backend.main:app --reload
```
                """)
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. API is not responding.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============ TAB 3: MOOD HISTORY ============
with tab3:
    st.markdown("## Your Mood History")
    
    st.write(f"**User ID:** `{st.session_state.user_id}`")
    
    st.markdown("")
    
    if st.button("📥 Load History", type="primary", key="load_history_btn", use_container_width=True):
        with st.spinner("Loading your mood history..."):
            try:
                response = requests.get(
                    f"{API_BASE}/api/mood-history/{st.session_state.user_id}",
                    params={"limit": 50, "offset": 0},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get('history', [])
                    
                    if entries:
                        st.success(f"✅ Found {data.get('total_count', 0)} mood entries")
                        
                        # Statistics Section
                        moods = [e.get('primary_mood', 'unknown') for e in entries]
                        mood_counts = Counter(moods)
                        
                        st.markdown("### 📊 Statistics")
                        stat_col1, stat_col2, stat_col3 = st.columns(3)
                        
                        with stat_col1:
                            st.metric("Total Entries", len(entries))
                        with stat_col2:
                            st.metric("Unique Moods", len(mood_counts))
                        with stat_col3:
                            most_common = mood_counts.most_common(1)[0][0].title() if mood_counts else "N/A"
                            st.metric("Most Common Mood", most_common)
                        
                        # Recent Entries
                        st.markdown("### 📜 Recent Entries")
                        
                        for idx, entry in enumerate(entries[:20], 1):
                            mood = entry.get('primary_mood', 'Unknown').title()
                            energy = entry.get('energy_level', 0)
                            date = entry.get('timestamp', 'N/A')[:10]
                            user_input = entry.get('user_input', '')
                            
                            with st.expander(f"**{idx}.** {mood} — {date}"):
                                st.write(f"**User Input:** {user_input[:100]}...")
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**Energy Level:** {energy}/10")
                                with col2:
                                    st.write(f"**Date:** {date}")
                    else:
                        st.info("📝 No history found. Generate playlists to start tracking your moods!")
                        
                elif response.status_code == 404:
                    st.warning("⚠️ No mood history found for this user. Start by generating your first playlist!")
                else:
                    st.error(f"❌ Error {response.status_code}: Unable to load history")
                    
            except requests.exceptions.ConnectionError:
                st.error("""
❌ **Backend API is not running**

Please start the backend server:
```bash
uvicorn app.backend.main:app --reload
```
                """)
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. API is not responding.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============ FOOTER ============
st.markdown("---")
st.markdown("""
<div class="footer">
    MusicMood © 2025 • Powered by AI
</div>
""", unsafe_allow_html=True)
