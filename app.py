import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import datetime
import pandas as pd

# Load secret credentials from Streamlit secrets
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(json_key)
client = gspread.authorize(creds)
import streamlit as st

# Get sheet name from Streamlit secrets for flexibility and security
SHEET_NAME = st.secrets.get("GOOGLE_SHEET_NAME", "AniGPT_DB")

try:
    sheet = client.open(SHEET_NAME)
except Exception as e:
    st.error(f"Failed to open Google Sheet '{SHEET_NAME}': {e}")
    sheet = None

# Define required tabs and their headers
tabs_info = {
    "Memory": ["Date", "User", "Memory"],
    "Mood logs": ["Date", "User", "Mood", "Trigger"],
    "Daily journal": ["Date", "User", "Summary", "Keywords"],
    "Learning": ["Date", "User", "WhatWasLearned", "Context"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "User", "Transcript"],
    "Anibook outline": ["Chapter", "Title", "Points", "User"],
    "Improvement notes": ["Date", "User", "Issue", "Solution"],
    "Quotes": ["Quote", "Author", "User"],
    "User facts": ["User", "Fact", "Date"],
    "Task done": ["Task", "Date", "Status", "User"],
    "Auto backup logs": ["Date", "User", "BackupInfo"]
}

# Ensure tabs exist with correct headers
for tab, headers in tabs_info.items():
    try:
        ws = sheet.worksheet(tab)
        current_headers = ws.row_values(1)
        if current_headers != headers:
            for i, h in enumerate(headers):
                ws.update_cell(1, i+1, h)
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title=tab, rows="100", cols="20")
        ws = sheet.worksheet(tab)
        ws.append_row(headers)

# Function to auto-detect tab
def detect_tab(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["happy", "sad", "angry", "depressed"]):
        return "Mood logs"
    elif any(word in text_lower for word in ["learn", "study", "course", "understood"]):
        return "Learning"
    elif any(word in text_lower for word in ["remind", "todo", "task", "due", "schedule"]):
        return "Reminders"
    elif any(word in text_lower for word in ["goal", "dream", "plan", "achieve"]):
        return "Life goals"
    elif any(word in text_lower for word in ["journal", "diary", "summary"]):
        return "Daily journal"
    elif any(word in text_lower for word in ["voice", "record", "said"]):
        return "Voice logs"
    elif any(word in text_lower for word in ["chapter", "outline", "story", "book"]):
        return "Anibook outline"
    elif any(word in text_lower for word in ["improve", "problem", "fix", "issue"]):
        return "Improvement notes"
    elif any(word in text_lower for word in ["quote", "inspire", "motivate"]):
        return "Quotes"
    elif any(word in text_lower for word in ["fact", "about me", "info"]):
        return "User facts"
    elif any(word in text_lower for word in ["done", "completed", "finished"]):
        return "Task done"
    elif any(word in text_lower for word in ["backup", "autosave"]):
        return "Auto backup logs"
    else:
        return "Memory"

# Streamlit UI
st.title("🧠 AniGPT v2.0 – Personal Learning Assistant")
user = st.selectbox("👤 Select user", ["Ani", "Anne"])
input_text = st.text_area("📝 Enter your update")

if st.button("💾 Save Entry"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        tab = detect_tab(input_text)
        ws = sheet.worksheet(tab)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare row based on tab headers
        headers = ws.row_values(1)
        row = []
        for header in headers:
            if "Date" in header:
                row.append(now)
            elif "User" in header:
                row.append(user)
            elif "Memory" in header or "Summary" in header or "Task" in header or "Transcript" in header or "Quote" in header or "BackupInfo" in header or "Fact" in header or "Goal" in header or "Issue" in header or "Chapter" in header or "Title" in header or "Points" in header or "Author" in header or "Context" in header or "WhatWasLearned" in header:
                row.append(input_text)
            else:
                row.append("")

        ws.append_row(row)
        st.success(f"✅ Saved to '{tab}' tab!")

