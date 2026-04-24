import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os

# 1. Page Configuration (Icon & Title)
st.set_page_config(page_title="Activity Tracker", page_icon="📈")

st.title("⏱️ Activity Tracker")

# 2. Activity Selection
activities = [
    "🎹 Piano Practice", 
    "📸 Photo Archiving", 
    "🌳 Family Research", 
    "💃 Line Dancing", 
    "🚶‍♂️ Walking", 
    "💪 Other Exercise", 
    "📖 Study"
]

selected_activity = st.selectbox("What are we working on?", activities)

# 3. Timer Logic
if 'running' not in st.session_state:
    st.session_state.running = False
    st.session_state.start_time = None

col1, col2 = st.columns(2)

if not st.session_state.running:
    if col1.button("▶️ START", use_container_width=True):
        st.session_state.running = True
        st.session_state.start_time = datetime.now()
        st.rerun()
else:
    if col1.button("⏹️ STOP & SAVE", use_container_width=True):
        end_time = datetime.now()
        duration = end_time - st.session_state.start_time
        duration_minutes = round(duration.total_seconds() / 60, 2)
        
        new_entry = {
            "Date": st.session_state.start_time.strftime("%Y-%m-%d"),
            "Activity": selected_activity,
            "Start": st.session_state.start_time.strftime("%I:%M %p"),
            "End": end_time.strftime("%I:%M %p"),
            "Minutes": duration_minutes
        }
        
        df_new = pd.DataFrame([new_entry])
        df_new.to_csv("activity_log.csv", mode='a', index=False, header=not os.path.exists("activity_log.csv"))
        
        st.success(f"Saved: {duration_minutes} mins")
        st.session_state.running = False
        st.session_state.start_time = None
        st.rerun()

# 4. Live Timer Display
if st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
    st.metric("Elapsed Time", f"{str(elapsed).split('.')[0]}")
    st.info(f"Currently logging: {selected_activity}")
    time.sleep(1)
    st.rerun()

# 5. Recent Activity Log (The Table)
st.divider()
st.subheader("📜 Recent Activity")

if os.path.exists("activity_log.csv"):
    history_df = pd.read_csv("activity_log.csv")
    # Show the last 10 entries, newest at the top
    st.dataframe(history_df.iloc[::-1].head(10), use_container_width=True, hide_index=True)
else:
    st.write("No logs yet. Start your first activity!")