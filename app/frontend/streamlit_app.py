"""
MusicMood Streamlit Frontend - Royal Edition (Cleaned & Simplified)
Main application entry point with multi-page navigation
"""

import streamlit as st
import requests
from typing import Optional, Dict, Any

# Page configuration
st.set_page_config(
    page_title="MusicMood - Royal AI Playlist",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Royal Dark Theme CSS - Simplified & Clean
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@400;500;600&display=swap');
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #2d1b4e 100%);
        background-attachment: fixed;
    }
    
    /* Royal buttons */
    .stButton>button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%) !important;
        color: #ffd700 !important;
        border: 2px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 10px !important;
        font-family: 'Cinzel', serif !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        padding: 12px 28px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(139, 92, 246, 0.6) !important;
    }
    
    /* Headings */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #ffd700 !important;
        letter-spacing: 1.5px !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.3) !important;
    }
    
    h1 { font-size: 3.2rem !important; font-weight: 700 !important; }
    h2 { font-size: 2.4rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.8rem !important; font-weight: 600 !important; }
    
    /* Body text */
    p, label, div, .stMarkdown {
        font-family: 'Cormorant Garamond', serif !important;
        color: #e0e7ff !important;
        font-size: 1.2rem !important;
        line-height: 1.7 !important;
    }
    
    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background: rgba(26, 31, 58, 0.9) !important;
        border: 2px solid rgba(139, 92, 246, 0.5) !important;
        border-radius: 10px !important;
        color: #e0e7ff !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 1.1rem !important;
        padding: 12px 14px !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.99) 0%, rgba(26, 31, 58, 0.99) 100%) !important;
        border-right: 3px solid rgba(255, 215, 0, 0.4) !important;
    }
    
    /* Hide Streamlit footer */
    footer { display: none !important; }
    
</style>
""", unsafe_allow_html=True)

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "anonymous"


def check_api_health() -> bool:
    """Check if API is online"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def display_home():
    """Display home page"""
    
    # Hero
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='font-size: 3.5rem;'>👑 MusicMood Royal</h1>
            <p style='font-size: 1.4rem; color: #c4b5fd;'>
                AI-Powered Mood-Based Playlist Generator
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='background: rgba(139, 92, 246, 0.15); padding: 2rem; 
                        border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3);'>
                <h3 style='text-align: center;'>🧠 Smart AI</h3>
                <p style='text-align: center; font-size: 1.1rem;'>
                    Your mood, understood. Your music, perfected.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: rgba(139, 92, 246, 0.15); padding: 2rem; 
                        border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3);'>
                <h3 style='text-align: center;'>🎵 Spotify</h3>
                <p style='text-align: center; font-size: 1.1rem;'>
                    Millions of tracks at your fingertips.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: rgba(139, 92, 246, 0.15); padding: 2rem; 
                        border-radius: 12px; border: 1px solid rgba(139, 92, 246, 0.3);'>
                <h3 style='text-align: center;'>⚡ Instant</h3>
                <p style='text-align: center; font-size: 1.1rem;'>
                    Your playlist, ready in moments.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CTA
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎵 Generate Your Playlist", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🎵_Generate_Playlist.py")


def display_sidebar():
    """Display sidebar"""
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 2rem 0;'>
                <h2 style='font-size: 2rem; margin: 0;'>👑 MusicMood</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User ID
        user_id = st.text_input(
            "User ID:",
            value=st.session_state.user_id,
            help="Your unique identifier",
            key="sidebar_user"
        )
        st.session_state.user_id = user_id
        
        st.markdown("---")
        
        # API Status
        is_online = check_api_health()
        status = "✅ Online" if is_online else "❌ Offline"
        st.markdown(f"**API Status:** {status}")
        
        st.markdown("---")
        
        st.markdown("""
            <p style='font-size: 1rem; color: #a78bfa; text-align: center;'>
                Made with ❤️ using FastAPI & Ollama
            </p>
        """, unsafe_allow_html=True)


def main():
    """Main app"""
    display_sidebar()
    display_home()


if __name__ == "__main__":
    main()
