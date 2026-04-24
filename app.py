import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Activity Tracker", page_icon="⏱️")
st.title("⏱️ Activity Tracker")

# 2. Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

activities = [
    "🎹 Piano Practice", "📸 Photo Archiving", "🌳 Family Research", 
    "💃 Line Dancing", "🚶‍♂️ Walking", "💪 Other Exercise", "📖 Study"
]

selected_activity = st.selectbox("What are we working on?", activities)

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
        
        new_entry = pd.DataFrame([{
            "Date": st.session_state.start_time.strftime("%Y-%m-%d"),
            "Activity": selected_activity,
            "Start": st.session_state.start_time.strftime("%I:%M %p"),
            "End": end_time.strftime("%I:%M %p"),
            "Minutes": duration_minutes
        }])
        
        # Pull existing data, add new row, and upload
        existing_data = conn.read()
        updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(data=updated_df)
        
        st.success(f"Saved: {duration_minutes} mins")
        st.session_state.running = False
        st.session_state.start_time = None
        st.rerun()

if st.session_state.running:
    elapsed = datetime.now() - st.session_state.start_time
    st.metric("Elapsed Time", f"{str(elapsed).split('.')[0]}")
    time.sleep(1)
    st.rerun()

st.divider()
st.subheader("📜 Recent Activity")
try:
    history_df = conn.read()
    st.dataframe(history_df.iloc[::-1].head(10), use_container_width=True, hide_index=True)
except:
    st.write("Check your Google Sheet connection in Secrets.")
