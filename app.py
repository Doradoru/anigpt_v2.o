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

# 3️⃣ Open Sheet via URL (this avoids 'not found' error)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1UIYuoQRhRfR1rjoy-6jHK5tLyCso-3fBvqLtSTv3-lc"
try:
    sheet = client.open_by_url(SHEET_URL)
    st.success("✅ Connected to AniGPT_DB Google Sheet")
except Exception as e:
    st.error(f"❌ Failed to open Google Sheet.\n\n{e}")
    st.stop()

# 4️⃣ Define all required tabs and their headers (Ani + Anne)
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

    # 🔮 Smart future tabs:
    "Behavior Patterns": ["Date", "User", "Pattern", "Emotion", "Trigger", "Notes"],
    "Skill Tracker": ["Date", "User", "Skill", "Level", "Practice Time", "Resource Used"],
    "AI Feedback": ["Date", "User", "Feedback Type", "Message", "Context"],
    "Command History": ["Date", "User", "Command", "Result", "Status"],
    "Gratitude Logs": ["Date", "User", "Gratitude 1", "Gratitude 2", "Gratitude 3"],
    "Relationship Journal": ["Date", "Type", "Summary", "Emotion", "Action Taken", "User"]
}

# 5️⃣ Create/update all tabs
created, updated = [], []
existing_tabs = [ws.title for ws in sheet.worksheets()]

for tab, headers in tabs.items():
    if tab not in existing_tabs:
        ws = sheet.add_worksheet(title=tab, rows="100", cols=str(len(headers)))
        ws.insert_row(headers, 1)
        created.append(tab)
    else:
        ws = sheet.worksheet(tab)
        current_headers = ws.row_values(1)
        missing = [h for h in headers if h not in current_headers]
        for h in missing:
            ws.update_cell(1, len(current_headers) + 1, h)
            current_headers.append(h)
        if missing:
            updated.append(f"{tab} (+{len(missing)} columns)")

# 6️⃣ Summary to user
if created:
    st.success(f"🆕 Tabs Created: {', '.join(created)}")
if updated:
    st.info(f"🛠️ Tabs Updated: {', '.join(updated)}")
if not created and not updated:
    st.success("✅ All tabs and headers are already perfect!")

st.caption("📌 AniGPT setup complete. Ready to log data and train the assistant! 🚀")
