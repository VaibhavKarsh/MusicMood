"""
Mood History Page
View mood analysis patterns and insights over time
"""

import streamlit as st
import sys
import os
from datetime import datetime
from collections import Counter

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import get_api_client
from ui_utils import get_mood_emoji, display_error

# Initialize API client
api = get_api_client()

st.title("📊 Mood History")
st.markdown("Track your emotional journey through music!")

# Get user ID
user_id = st.session_state.get('user_id', 'anonymous')

st.markdown(f"**User:** {user_id}")

# Fetch mood history
try:
    with st.spinner("Loading your mood history..."):
        response = api.get_mood_history(
            user_id=user_id,
            limit=100,  # Get more for analytics
            offset=0
        )
    
    entries = response.get('entries', [])
    total = response.get('total', 0)
    
    if not entries:
        st.info("🎭 No mood history yet. Generate a playlist to start tracking your moods!")
        
        if st.button("🚀 Generate Playlist", type="primary"):
            st.switch_page("pages/1_🎵_Generate_Playlist.py")
        
        st.stop()
    
    # Summary metrics
    st.markdown("---")
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", total)
    
    with col2:
        moods = [e.get('detected_emotion', 'unknown') for e in entries]
        most_common = max(set(moods), key=moods.count) if moods else 'N/A'
        emoji = get_mood_emoji(most_common)
        st.metric("Most Common Mood", f"{emoji} {most_common.capitalize()}")
    
    with col3:
        confidences = [e.get('confidence_score', 0) for e in entries if e.get('confidence_score')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        st.metric("Avg Confidence", f"{avg_confidence:.0%}")
    
    with col4:
        times_of_day = [e.get('time_of_day', 'unknown') for e in entries]
        most_active_time = max(set(times_of_day), key=times_of_day.count) if times_of_day else 'N/A'
        time_emojis = {'morning': '🌅', 'afternoon': '☀️', 'evening': '🌆', 'night': '🌙'}
        time_emoji = time_emojis.get(most_active_time, '🕐')
        st.metric("Most Active Time", f"{time_emoji} {most_active_time.capitalize()}")
    
    st.markdown("---")
    
    # Mood distribution
    st.markdown("### 🎭 Mood Distribution")
    
    mood_counts = Counter(moods)
    
    if mood_counts:
        # Create a simple bar chart visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display as progress bars
            for mood, count in mood_counts.most_common():
                percentage = (count / len(moods)) * 100
                emoji = get_mood_emoji(mood)
                
                st.markdown(f"**{emoji} {mood.capitalize()}**")
                st.progress(percentage / 100)
                st.caption(f"{count} entries ({percentage:.1f}%)")
                st.markdown("")
        
        with col2:
            st.markdown("**Top 5 Moods:**")
            for idx, (mood, count) in enumerate(mood_counts.most_common(5), 1):
                emoji = get_mood_emoji(mood)
                st.markdown(f"{idx}. {emoji} **{mood.capitalize()}**: {count}")
    
    st.markdown("---")
    
    # Time of day analysis
    st.markdown("### 🕐 Time of Day Patterns")
    
    time_counts = Counter(times_of_day)
    
    if time_counts:
        col1, col2, col3, col4 = st.columns(4)
        
        time_data = {
            'morning': ('�', 'Morning', col1),
            'afternoon': ('☀️', 'Afternoon', col2),
            'evening': ('🌆', 'Evening', col3),
            'night': ('🌙', 'Night', col4)
        }
        
        for time_key, (emoji, label, col) in time_data.items():
            with col:
                count = time_counts.get(time_key, 0)
                percentage = (count / len(times_of_day)) * 100 if times_of_day else 0
                st.metric(f"{emoji} {label}", count)
                st.caption(f"{percentage:.1f}% of entries")
    
    st.markdown("---")
    
    # Recent entries timeline
    st.markdown("### � Recent Mood Timeline")
    
    # Display recent entries
    display_limit = st.slider("Show entries:", 5, min(50, len(entries)), 10)
    
    recent_entries = entries[:display_limit]
    
    for idx, entry in enumerate(recent_entries, 1):
        with st.container():
            col1, col2, col3 = st.columns([0.5, 2, 1])
            
            with col1:
                mood = entry.get('detected_emotion', 'unknown')
                emoji = get_mood_emoji(mood)
                st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{emoji}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{mood.capitalize()}** Mood")
                
                mood_text = entry.get('mood_text', 'No description')
                if len(mood_text) > 100:
                    mood_text = mood_text[:100] + "..."
                st.caption(f'"{mood_text}"')
                
                # Timestamp
                created = entry.get('created_at')
                if created:
                    try:
                        if isinstance(created, str):
                            created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                            st.caption(f"📅 {created_dt.strftime('%B %d, %Y at %I:%M %p')}")
                    except:
                        st.caption(f"📅 {created}")
            
            with col3:
                confidence = entry.get('confidence_score', 0)
                time_of_day = entry.get('time_of_day', 'unknown')
                
                st.metric("Confidence", f"{confidence:.0%}")
                time_emoji = time_emojis.get(time_of_day, '🕐')
                st.caption(f"{time_emoji} {time_of_day.capitalize()}")
            
            st.divider()
    
    if len(entries) > display_limit:
        st.caption(f"Showing {display_limit} of {len(entries)} entries")
    
    st.markdown("---")
    
    # Insights
    st.markdown("### 💡 Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Mood Patterns:**")
        
        # Identify patterns
        if len(mood_counts) == 1:
            st.info(f"You've been consistently {list(mood_counts.keys())[0]}!")
        elif len(mood_counts) >= 3:
            st.info(f"You experience a diverse range of emotions. Most common: {most_common}")
        else:
            st.info(f"Your moods alternate between {' and '.join(mood_counts.keys())}")
    
    with col2:
        st.markdown("**Time Preferences:**")
        
        if most_active_time != 'N/A':
            time_messages = {
                'morning': "You're most active in the morning! Early bird gets the playlist 🐦",
                'afternoon': "Afternoon is your prime time for music discovery ☀️",
                'evening': "Evening vibes are your favorite! Perfect time to unwind 🌆",
                'night': "Night owl detected! Late night music sessions 🦉"
            }
            st.info(time_messages.get(most_active_time, "Keep exploring music!"))
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 🎯 Recommendations")
    
    # Based on mood history, suggest something
    if most_common in ['sad', 'anxious', 'stressed']:
        st.success("💡 Try generating a 'calm' or 'relaxed' playlist to balance your mood!")
    elif most_common in ['happy', 'excited', 'energetic']:
        st.success("💡 Keep the positive vibes going! You might also enjoy 'motivated' playlists.")
    else:
        st.success("💡 Explore different moods to discover new music genres and artists!")

except Exception as e:
    display_error(str(e))

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎭 Mood Legend")
    
    common_moods = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('excited', 'Excited'),
        ('focused', 'Focused'),
        ('relaxed', 'Relaxed'),
        ('motivated', 'Motivated')
    ]
    
    for mood_key, mood_label in common_moods:
        emoji = get_mood_emoji(mood_key)
        st.markdown(f"{emoji} **{mood_label}**")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #b3b3b3; font-size: 0.9rem;">
        <p>📊 Your mood is automatically tracked with each playlist generation</p>
        <p>🔒 All data is private and secure</p>
    </div>
    """,
    unsafe_allow_html=True
)
