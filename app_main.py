import streamlit as st
from utils import connect_to_sheet

st.set_page_config(page_title="AniGPT Dashboard", layout="wide")

# Check login
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

username = st.session_state.username
st.sidebar.success(f"🧠 Logged in as: {username}")
st.title(f"Welcome, {username} 👋 — Your AniGPT Dashboard")

# Connect to Sheet
sheet = connect_to_sheet()

# Tabs in Google Sheet
tabs = {
    "Memory": ["Date", "Message"],
    "Mood logs": ["Date", "Mood", "Trigger"],
    "Daily journal": ["Date", "Summary", "Keywords"],
    "Learning": ["Date", "WhatWasLearned", "Context"],
    "Reminders": ["Task", "Date", "Time", "Status"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress"],
    "Quotes": ["Quote", "SaidBy", "Tags"],
    "Task done": ["Date", "Task", "Details"]
}

# Show each tab
for tab_name, headers in tabs.items():
    with st.expander(f"📂 {tab_name}"):
        try:
            worksheet = sheet.worksheet(tab_name)
            data = worksheet.get_all_records()
            # Filter by username column if needed in future
            st.dataframe(data)
        except:
            st.error(f"❌ Could not load tab: {tab_name}")
