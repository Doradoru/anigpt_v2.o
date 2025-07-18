import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="AniGPT v2.0", layout="centered")
st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")

# ---------------------- Auth & Google Sheet Setup ----------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# ---------------------- Auto Tab Detection ----------------------
def detect_tab(text):
    text = text.lower()

    if any(word in text for word in ["mood", "feeling", "happy", "sad", "angry", "stressed", "emotional"]):
        return "Mood logs"

    elif any(word in text for word in ["learned", "learning", "today i learned", "study", "knowledge", "til"]):
        return "Learning"

    elif any(word in text for word in ["remind", "reminder", "todo", "to do", "task", "deadline"]):
        return "Reminders"

    elif any(word in text for word in ["goal", "target", "aim", "milestone", "achieve"]):
        return "Life goals"

    elif any(word in text for word in ["quote", "thought", "inspiration", "motivational"]):
        return "Quotes"

    elif any(word in text for word in ["journal", "diary", "today", "i felt", "i experienced"]):
        return "Daily journal"

    elif any(word in text for word in ["improve", "problem", "fix", "solution", "habit", "mistake"]):
        return "Improvement notes"

    elif any(word in text for word in ["voice", "audio", "call", "conversation"]):
        return "Voice logs"

    elif any(word in text for word in ["outline", "book", "structure", "chapters"]):
        return "Anibook outline"

    elif any(word in text for word in ["backup", "log", "savepoint"]):
        return "Auto backup logs"

    elif any(word in text for word in ["task done", "completed", "finished"]):
        return "Task done"

    elif any(word in text for word in ["my name", "about me", "i am", "i like", "personal detail"]):
        return "User facts"

    else:
        return "Memory"

# ---------------------- Input Section ----------------------
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
user_input = st.text_area("✍️ What's on your mind?", height=150)
submit = st.button("💾 Save to Google Sheet")

# ---------------------- Tab Structures ----------------------
tab_columns = {
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Transcript", "User"],
    "Anibook outline": ["Title", "Points", "User"],
    "Improvement notes": ["Date", "Issue", "Solution", "User"],
    "Quotes": ["Quote", "Author", "User"],
    "User facts": ["Fact", "User"],
    "Task done": ["Task", "Date", "User"],
    "Auto backup logs": ["Backup Name", "Date", "User"],
    "Memory": ["Date", "Note", "User"]
}

# ---------------------- Ensure All Tabs Exist ----------------------
def ensure_tabs():
    existing_tabs = [ws.title for ws in sheet.worksheets()]
    for tab in tab_columns:
        if tab not in existing_tabs:
            sheet.add_worksheet(title=tab, rows="100", cols=str(len(tab_columns[tab])))
            sheet.worksheet(tab).append_row(tab_columns[tab])

ensure_tabs()

# ---------------------- Save to Sheet ----------------------
if submit and user_input.strip() != "":
    tab = detect_tab(user_input)
    worksheet = sheet.worksheet(tab)
    row_data = []

    today = datetime.now().strftime("%Y-%m-%d")

    if tab == "Mood logs":
        mood = "happy" if "happy" in user_input.lower() else "unknown"
        trigger = user_input
        row_data = [today, mood, trigger, user]

    elif tab == "Daily journal":
        row_data = [today, user_input, "general", user]

    elif tab == "Learning":
        row_data = [today, user_input, user, user]

    elif tab == "Reminders":
        row_data = [user_input, today, "00:00", "pending", user]

    elif tab == "Life goals":
        row_data = [user_input, "General", "2025-12-31", "0%", user]

    elif tab == "Voice logs":
        row_data = [today, user_input, user]

    elif tab == "Anibook outline":
        row_data = ["Untitled", user_input, user]

    elif tab == "Improvement notes":
        row_data = [today, "Issue: " + user_input, "Solution: TBD", user]

    elif tab == "Quotes":
        row_data = [user_input, "Unknown", user]

    elif tab == "User facts":
        row_data = [user_input, user]

    elif tab == "Task done":
        row_data = [user_input, today, user]

    elif tab == "Auto backup logs":
        row_data = ["AutoBackup", today, user]

    elif tab == "Memory":
        row_data = [today, user_input, user]

    worksheet.append_row(row_data)
    st.success(f"✅ Saved to '{tab}' tab!")
else:
    if submit:
        st.warning("⚠️ Please enter some text before submitting.")
