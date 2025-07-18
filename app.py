import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import re

st.set_page_config(page_title="AniGPT Input", layout="centered")
st.title("🧠 AniGPT Auto Entry – No Manual Selection Needed")

# Load secret key
json_key = st.secrets["GOOGLE_SHEET_JSON"]
if isinstance(json_key, str):
    json_key = json.loads(json_key)

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# Open Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1UIYuoQRhRfR1rjoy-6jHK5tLyCso-3fBvqLtSTv3-lc"
sheet = client.open_by_url(SHEET_URL)

# User selection only
user = st.selectbox("👤 Who's speaking?", ["Ani", "Anne"])
user_input = st.text_area("📥 What would you like to say/write? (Just type)")

# Intelligent type detection
def detect_type(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["happy", "sad", "angry", "neutral", "mood"]):
        return "Mood logs"
    elif any(word in text_lower for word in ["learn", "learned", "study", "course", "class"]):
        return "Learning"
    elif any(word in text_lower for word in ["remind", "tomorrow", "today", "meeting", "call", "task"]):
        return "Reminders"
    elif any(word in text_lower for word in ["quote", "inspire", "motivation"]):
        return "Quotes"
    elif any(word in text_lower for word in ["journal", "day", "diary", "summary"]):
        return "Daily journal"
    else:
        return "Memory"

# Auto-create tab + columns
def ensure_tab_and_columns(tab_name, data_dict):
    try:
        ws = sheet.worksheet(tab_name)
    except:
        ws = sheet.add_worksheet(title=tab_name, rows=100, cols=20)
        ws.append_row(list(data_dict.keys()))
    headers = ws.row_values(1)
    new_headers = [key for key in data_dict if key not in headers]
    for h in new_headers:
        ws.update_cell(1, len(headers)+1, h)
        headers.append(h)
    return ws, headers

# Smart form submit
if st.button("💾 Submit"):
    if user_input.strip() == "":
        st.warning("⚠️ Please type something.")
    else:
        entry_type = detect_type(user_input)
        data = {
            "User": user,
            "Date": datetime.today().strftime("%Y-%m-%d"),
            "Entry": user_input
        }

        try:
            ws, headers = ensure_tab_and_columns(entry_type, data)
            row = [data.get(h, "") for h in headers]
            ws.append_row(row)
            st.success(f"✅ Saved as '{entry_type}' for {user}")
        except Exception as e:
            st.error(f"❌ Failed to save: {e}")
