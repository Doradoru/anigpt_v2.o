import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Load service account info from secrets.toml
service_account_info = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
credentials = Credentials.from_service_account_info(service_account_info)

# Connect to Google Sheets
client = gspread.authorize(credentials)
sheet = client.open("AniGPT_DB")

# Define required sheet tabs
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders", "Life goals",
    "Voice logs", "Anibook outline", "Improvement notes", "Quotes",
    "User facts", "Task done", "Auto backup logs"
]

# Create missing tabs if needed
existing_tabs = [ws.title for ws in sheet.worksheets()]
for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows=1000, cols=20)

# Helper to detect type of input
def detect_input_type(user_input):
    lower_input = user_input.lower()
    if "mood:" in lower_input:
        return "Mood logs"
    elif "today i learned" in lower_input:
        return "Learning"
    elif "remind me" in lower_input or "reminder:" in lower_input:
        return "Reminders"
    elif "goal:" in lower_input:
        return "Life goals"
    elif "quote:" in lower_input:
        return "Quotes"
    elif "voice log:" in lower_input:
        return "Voice logs"
    elif "journal:" in lower_input:
        return "Daily journal"
    elif "memory:" in lower_input:
        return "Memory"
    elif "done:" in lower_input:
        return "Task done"
    elif "fact:" in lower_input:
        return "User facts"
    elif "improve:" in lower_input:
        return "Improvement notes"
    elif "anibook:" in lower_input:
        return "Anibook outline"
    else:
        return "Memory"

# Helper to save to sheet
def save_to_sheet(tab, data):
    ws = sheet.worksheet(tab)
    ws.append_row(data)

# Streamlit UI
st.set_page_config(page_title="🧠 AniGPT v2", page_icon="🤖")
st.title("🧠 AniGPT - Your Self-Learning AI Assistant")

user_input = st.text_area("What would you like to share today?", height=150)

if st.button("➕ Save"):
    if user_input.strip() == "":
        st.warning("Please write something before saving.")
    else:
        tab = detect_input_type(user_input)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format data based on tab type
        if tab == "Mood logs":
            mood = user_input.split("mood:")[-1].strip()
            save_to_sheet(tab, [now.split(" ")[0], mood, ""])
        elif tab == "Learning":
            save_to_sheet(tab, [now.split(" ")[0], user_input, "User input"])
        elif tab == "Reminders":
            save_to_sheet(tab, [user_input, now.split(" ")[0], now.split(" ")[1], "Pending"])
        elif tab == "Life goals":
            save_to_sheet(tab, [user_input, "Personal", "", "Not started"])
        elif tab == "Daily journal":
            save_to_sheet(tab, [now.split(" ")[0], user_input, "User journal"])
        elif tab == "Quotes":
            save_to_sheet(tab, [user_input])
        elif tab == "Task done":
            save_to_sheet(tab, [user_input, now.split(" ")[0]])
        elif tab == "Voice logs":
            save_to_sheet(tab, [now, user_input])
        elif tab == "Anibook outline":
            save_to_sheet(tab, [now, user_input])
        elif tab == "User facts":
            save_to_sheet(tab, [user_input])
        elif tab == "Improvement notes":
            save_to_sheet(tab, [now, user_input])
        elif tab == "Memory":
            save_to_sheet(tab, [now, user_input])
        else:
            save_to_sheet("Memory", [now, user_input])

        st.success(f"Saved to **{tab}** tab ✅")
