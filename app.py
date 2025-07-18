import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

st.set_page_config(page_title="AniGPT v2.0", layout="centered")
st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")
st.markdown("Write anything. I'll auto-detect where to save it. You're free now, Ani. 😎")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# Ensure all required tabs exist
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "Quotes", "User facts", "Task done", "Auto backup logs"
]
existing_tabs = [ws.title for ws in sheet.worksheets()]
for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows="1000", cols="20")

# Function to detect tab
def detect_tab(text):
    text = text.lower()
    if any(word in text for word in ["mood", "happy", "sad", "stress"]):
        return "Mood logs"
    elif any(word in text for word in ["learned", "learning", "til", "study"]):
        return "Learning"
    elif any(word in text for word in ["remind", "reminder", "task", "todo"]):
        return "Reminders"
    elif any(word in text for word in ["goal", "target", "dream"]):
        return "Life goals"
    elif any(word in text for word in ["quote", "thought", "inspiration"]):
        return "Quotes"
    elif any(word in text for word in ["journal", "today", "i felt"]):
        return "Daily journal"
    elif any(word in text for word in ["improve", "problem", "habit"]):
        return "Improvement notes"
    else:
        return "Memory"

# 🧑 User dropdown + Input
st.header("📥 Input Entry")
user_name = st.selectbox("👤 Who are you?", ["Ani", "Anne"])
entry_text = st.text_area("📝 Type your message... I'll auto-categorize it.")
submit = st.button("💾 Auto Save")

# Save logic
if submit and entry_text.strip() != "":
    entry_type = detect_tab(entry_text)
    sheet_tab = sheet.worksheet(entry_type)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
