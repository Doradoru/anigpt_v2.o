import streamlit as st
import gspread
from datetime import datetime
import json
from google.oauth2.service_account import Credentials
import re

# Setup
st.set_page_config(page_title="AniGPT Input", layout="centered")
st.title("🧠 AniGPT Smart Input v2.0")

# Google Sheet Auth
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(json_key, scopes=scopes)
client = gspread.authorize(credentials)

# Sheet Setup
sheet = client.open("AniGPT_DB")

# All Tabs with Expected Headers
tabs_with_headers = {
    "Memory": ["Date", "Memory", "User"],
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Voice Input", "User"],
    "Anibook outline": ["Date", "Chapter", "Summary", "User"],
    "Improvement notes": ["Date", "Note", "User"],
    "Quotes": ["Date", "Quote", "User"],
    "User facts": ["Date", "Fact", "User"],
    "Task done": ["Task", "Date", "User"],
    "Auto backup logs": ["Date", "Backup Type", "Details", "User"]
}

# Ensure Tabs Exist
for tab, headers in tabs_with_headers.items():
    try:
        sheet.worksheet(tab)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title=tab, rows="100", cols="20")
        ws.append_row(headers)

# User Dropdown
user = st.selectbox("👤 Select User", ["Ani", "Anne"])

# Input box
input_text = st.text_area("✍️ Enter anything (Mood, Memory, Journal, Learning etc.)")

# Auto-tab detection function
def detect_tab(text):
    text = text.lower()
    if any(word in text for word in ["happy", "sad", "angry", "mood", "irritated"]):
        return "Mood logs"
    elif any(word in text for word in ["learned", "learning", "study", "padhai"]):
        return "Learning"
    elif any(word in text for word in ["goal", "dream", "life goal", "aim"]):
        return "Life goals"
    elif any(word in text for word in ["remind", "task", "tomorrow", "reminder"]):
        return "Reminders"
    elif any(word in text for word in ["quote", "motivation"]):
        return "Quotes"
    elif any(word in text for word in ["today", "journal", "experience", "routine"]):
        return "Daily journal"
    elif any(word in text for word in ["chapter", "book", "anibook"]):
        return "Anibook outline"
    elif any(word in text for word in ["improve", "growth", "better"]):
        return "Improvement notes"
    elif any(word in text for word in ["voice", "said", "record"]):
        return "Voice logs"
    elif any(word in text for word in ["fact", "birthday", "personal"]):
        return "User facts"
    elif any(word in text for word in ["done", "completed", "finished"]):
        return "Task done"
    else:
        return "Memory"

# Submit Button
if st.button("💾 Save to Google Sheet"):
    if input_text.strip() == "":
        st.warning("Please enter something first.")
    else:
        tab = detect_tab(input_text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = []

        # Prepare row based on tab
        if tab == "Mood logs":
            row = [now, "Auto", input_text, user]
        elif tab == "Daily journal":
            row = [now, input_text, "Auto", user]
        elif tab == "Learning":
            row = [now, input_text, "Context not set", user]
        elif tab == "Reminders":
            row = [input_text, now, "Time?", "Pending", user]
        elif tab == "Life goals":
            row = [input_text, "Life", "Later", "0%", user]
        elif tab == "Voice logs":
            row = [now, input_text, user]
        elif tab == "Anibook outline":
            row = [now, "Chapter ?", input_text, user]
        elif tab == "Improvement notes":
            row = [now, input_text, user]
        elif tab == "Quotes":
            row = [now, input_text, user]
        elif tab == "User facts":
            row = [now, input_text, user]
        elif tab == "Task done":
            row = [input_text, now, user]
        elif tab == "Auto backup logs":
            row = [now, "Auto", input_text, user]
        else:  # Memory
            row = [now, input_text, user]

        try:
            ws = sheet.worksheet(tab)
            ws.append_row(row)
            st.success(f"Saved to ➤ `{tab}` tab successfully! ✅")
        except Exception as e:
            st.error(f"Failed to save: {e}")
