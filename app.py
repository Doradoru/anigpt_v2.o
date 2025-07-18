import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

st.set_page_config(page_title="AniGPT v2.0", layout="centered")
st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")
st.markdown("Start journaling, saving thoughts, or giving commands. Your AI twin is listening...")

# Load credentials securely from secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("AniGPT_DB")

# Required tabs
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "Quotes", "User facts", "Task done", "Auto backup logs"
]

# Auto-create missing tabs
existing_tabs = [ws.title for ws in sheet.worksheets()]
for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows="1000", cols="20")

# Input UI
st.header("📥 Add Entry")
user_name = st.text_input("👤 Your Name (Ani / Anne)")
entry_type = st.selectbox("📂 Entry Type", required_tabs)
entry_text = st.text_area("📝 Your Input")
submit = st.button("💾 Save to Google Sheet")

# Handle submission
if submit and entry_text.strip() != "":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet_tab = sheet.worksheet(entry_type)

    # Save based on type
    if entry_type == "Mood logs":
        sheet_tab.append_row([timestamp, entry_text, user_name])
    elif entry_type == "Daily journal":
        sheet_tab.append_row([timestamp, entry_text, "keywords"])
    elif entry_type == "Learning":
        sheet_tab.append_row([timestamp, entry_text, "context"])
    elif entry_type == "Reminders":
        sheet_tab.append_row([entry_text, timestamp, "12:00 PM", "pending"])
    elif entry_type == "Life goals":
        sheet_tab.append_row([entry_text, "Career", "2025-12-31", "0%"])
    else:
        sheet_tab.append_row([timestamp, entry_text, user_name])

    st.success(f"✅ Saved to '{entry_type}' tab for {user_name}")
