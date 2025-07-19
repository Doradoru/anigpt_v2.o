import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# ====== SETUP SECRETS ======
json_key = st.secrets["GOOGLE_SHEET_JSON"]
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# ====== SHEET SETUP ======
SHEET_NAME = "AniGPT_DB"
TAB_SCHEMAS = {
    "Memory": ["Date", "Memory", "User"],
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Transcript", "Duration", "User"],
    "Anibook outline": ["Chapter", "Title", "Summary", "User"],
    "Improvement notes": ["Date", "Note", "User"],
    "Quotes": ["Quote", "User"],
    "User facts": ["Fact", "User"],
    "Task done": ["Date", "Task", "Result", "User"],
    "Auto backup logs": ["Date", "Data Type", "Status", "User"]
}

# ====== AUTO CREATE MISSING TABS ======
def ensure_tabs():
    spreadsheet = client.open(SHEET_NAME)
    sheet_titles = [ws.title for ws in spreadsheet.worksheets()]
    for tab, headers in TAB_SCHEMAS.items():
        if tab not in sheet_titles:
            ws = spreadsheet.add_worksheet(title=tab, rows="1000", cols="20")
            ws.append_row(headers)
        else:
            ws = spreadsheet.worksheet(tab)
            current_headers = ws.row_values(1)
            for i, h in enumerate(TAB_SCHEMAS[tab]):
                if i >= len(current_headers) or current_headers[i] != h:
                    ws.update_cell(1, i + 1, h)

ensure_tabs()

# ====== SMART TAB DETECTION FUNCTION ======
def detect_tab(text):
    t = text.lower()
    if any(word in t for word in ["sad", "happy", "mood", "tension"]):
        return "Mood logs"
    elif any(word in t for word in ["learn", "seekha", "pada", "study"]):
        return "Learning"
    elif any(word in t for word in ["goal", "dream", "target"]):
        return "Life goals"
    elif any(word in t for word in ["remind", "yaad dilana", "kal", "subah"]):
        return "Reminders"
    elif any(word in t for word in ["summary", "day", "journal"]):
        return "Daily journal"
    elif any(word in t for word in ["quote", "soch", "vichar"]):
        return "Quotes"
    elif any(word in t for word in ["voice", "audio", "recording"]):
        return "Voice logs"
    elif any(word in t for word in ["chapter", "book", "ani book"]):
        return "Anibook outline"
    elif any(word in t for word in ["improve", "change", "habit"]):
        return "Improvement notes"
    elif any(word in t for word in ["task", "complete", "done"]):
        return "Task done"
    elif any(word in t for word in ["fact", "personal", "about"]):
        return "User facts"
    elif any(word in t for word in ["backup", "auto", "saved"]):
        return "Auto backup logs"
    else:
        return "Memory"

# ====== UI ======
st.title("🧠 AniGPT v2 – Smart Data Entry")
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
input_text = st.text_area("📝 Enter your input")

submit = st.button("💾 Save Entry")

if submit and input_text:
    detected_tab = detect_tab(input_text)
    ws = client.open(SHEET_NAME).worksheet(detected_tab)
    headers = ws.row_values(1)

    now = datetime.now().strftime("%Y-%m-%d")

    # Smart mapping based on schema
    row = []
    for h in headers:
        if h == "Date":
            row.append(now)
        elif h == "User":
            row.append(user)
        else:
            row.append(input_text)  # default fill with full input

    ws.append_row(row)
    st.success(f"✅ Saved to '{detected_tab}' tab successfully!")
