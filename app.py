import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

st.set_page_config(page_title="🧠 AniGPT Setup", layout="centered")
st.title("🧠 AniGPT – Auto Tab Setup & Sheet Sync")

# 1️⃣ Load credentials from Streamlit secrets
json_key = st.secrets["GOOGLE_SHEET_JSON"]
if isinstance(json_key, str):
    json_key = json.loads(json_key)

# 2️⃣ Authorize with Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# 3️⃣ Open Google Sheet
SHEET_NAME = "AniGPT_DB"
try:
    sheet = client.open("AniGPT_DB")

    st.success(f"✅ Connected to Sheet: {SHEET_NAME}")
except:
    st.error(f"❌ Failed to open sheet: {SHEET_NAME}")
    st.stop()

# 4️⃣ Define Tabs + Headers (including smart futuristic ones)
tabs = {
    "Memory": ["Date", "Input", "Response", "User"],
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Command", "Action", "User"],
    "Anibook outline": ["Date", "Topic", "Subpoints", "User"],
    "Improvement notes": ["Date", "Observation", "Improvement", "User"],
    "Quotes": ["Date", "Quote", "Source", "User"],
    "User facts": ["Fact", "Context", "User"],
    "Task done": ["Task", "Date", "User"],
    "Auto backup logs": ["Date", "Action", "User"],

    # 🧠 Advanced Tabs
    "Behavior Patterns": ["Date", "User", "Pattern", "Emotion", "Trigger", "Notes"],
    "Skill Tracker": ["Date", "User", "Skill", "Level", "Practice Time", "Resource Used"],
    "AI Feedback": ["Date", "User", "Feedback Type", "Message", "Context"],
    "Command History": ["Date", "User", "Command", "Result", "Status"],
    "Gratitude Logs": ["Date", "User", "Gratitude 1", "Gratitude 2", "Gratitude 3"],
    "Relationship Journal": ["Date", "Type", "Summary", "Emotion", "Action Taken", "User"]
}

# 5️⃣ Auto-create/update tabs & headers
existing_tabs = [ws.title for ws in sheet.worksheets()]
created, updated = [], []

for tab, headers in tabs.items():
    if tab not in existing_tabs:
        ws = sheet.add_worksheet(title=tab, rows="100", cols=str(len(headers)))
        ws.insert_row(headers, 1)
        created.append(tab)
    else:
        ws = sheet.worksheet(tab)
        existing_headers = ws.row_values(1)
        missing = [h for h in headers if h not in existing_headers]
        for m in missing:
            ws.update_cell(1, len(existing_headers)+1, m)
            existing_headers.append(m)
        if missing:
            updated.append(f"{tab} (+{len(missing)} columns)")

# 6️⃣ Output summary to user
if created:
    st.success(f"🆕 Tabs Created: {', '.join(created)}")
if updated:
    st.info(f"🛠️ Tabs Updated: {', '.join(updated)}")
if not created and not updated:
    st.success("✅ All tabs and headers are already perfect!")

st.caption("📌 AniGPT v2 sheet setup complete. Continue building Jarvis... 🚀")
