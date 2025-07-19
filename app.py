import streamlit as st
import gspread
import json
from datetime import datetime
from google.oauth2.service_account import Credentials

# Load credentials from Streamlit secrets
json_key = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(json_key)
client = gspread.authorize(creds)

# Open sheet
sheet = client.open("AniGPT_DB")

# Tabs and their required headers
tabs = {
    "Memory": ["Date", "Memory", "User"],
    "Mood logs": ["Date", "Mood", "Trigger", "User"],
    "Daily journal": ["Date", "Summary", "Keywords", "User"],
    "Learning": ["Date", "WhatWasLearned", "Context", "User"],
    "Reminders": ["Task", "Date", "Time", "Status", "User"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress", "User"],
    "Voice logs": ["Date", "Transcript", "User"],
    "Anibook outline": ["Chapter", "Topic", "Summary", "User"],
    "Improvement notes": ["Area", "Suggestion", "User"],
    "Quotes": ["Quote", "Author", "User"],
    "User facts": ["Fact", "Context", "User"],
    "Task done": ["Task", "Date", "User"],
    "Auto backup logs": ["Date", "Backup Type", "Status", "User"],
    "Users": ["Name", "Password", "Created"]
}

# Auto-create missing tabs
for tab_name, headers in tabs.items():
    try:
        ws = sheet.worksheet(tab_name)
    except:
        ws = sheet.add_worksheet(title=tab_name, rows=100, cols=len(headers))
    try:
        existing = ws.row_values(1)
        if existing != headers:
            ws.delete_rows(1)
            ws.insert_row(headers, 1)
    except:
        ws.insert_row(headers, 1)

# User selection
st.title("AniGPT v2.0 🧠")
user = st.selectbox("👤 Choose User", ["Ani", "Anne"])

# Input
text = st.text_area("📝 Enter your message or log")

# Auto tab detection logic
def detect_tab(text):
    keywords = {
        "Mood logs": ["sad", "happy", "angry", "irritated"],
        "Daily journal": ["aaj", "subah", "raat", "jaana", "kiya"],
        "Learning": ["seekha", "sikh", "learn", "padh", "study"],
        "Reminders": ["yaad", "bhool", "kaam", "meeting", "alarm"],
        "Life goals": ["goal", "dream", "future", "plan"],
        "Voice logs": ["audio", "voice", "recorded"],
        "Anibook outline": ["chapter", "book", "novel", "pustak"],
        "Improvement notes": ["improve", "sudhar", "better"],
        "Quotes": ["quote", "inspiration", "motivation"],
        "User facts": ["mera", "main", "mujhe", "habit"],
        "Task done": ["complete", "done", "finish"],
        "Memory": ["yaad", "memory", "recall"]
    }
    for tab, keys in keywords.items():
        if any(k in text.lower() for k in keys):
            return tab
    return "Memory"

# Save button
if st.button("💾 Save"):
    if not text:
        st.warning("Please enter some text.")
    else:
        tab = detect_tab(text)
        ws = sheet.worksheet(tab)
        headers = ws.row_values(1)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build row based on headers
        row = []
        for h in headers:
            if h.lower() == "date":
                row.append(now)
            elif h.lower() == "user":
                row.append(user)
            elif h.lower() == "status":
                row.append("Pending")
            elif h.lower() == "task":
                row.append(text if "remind" in tab.lower() else "")
            elif h.lower() == "summary" or h.lower() == "memory" or h.lower() == "quote":
                row.append(text)
            else:
                row.append("")

        ws.append_row(row)
        st.success(f"Saved to **{tab}** successfully! ✅")
