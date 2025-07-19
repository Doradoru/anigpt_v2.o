import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz

# ---------- SETUP ----------
st.set_page_config(page_title="AniGPT Day 8", layout="centered")

# ---------- AUTH ----------
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(
    st.secrets["GOOGLE_SHEET_JSON"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# ---------- CHECK + CREATE TABS ----------
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "Quotes", "User facts", "Task done", "Auto backup logs"
]
existing_tabs = [ws.title for ws in sheet.worksheets()]

for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows=1000, cols=10)

st.success("✅ Connected to AniGPT_DB and Tabs Verified")

# ---------- DATE ----------
india = pytz.timezone("Asia/Kolkata")
now = datetime.now(india)
today = now.strftime("%d-%m-%Y")

# ---------- MOOD LOGGER ----------
st.header("🧠 AniGPT - Mood Logger")

mood = st.selectbox("😌 How are you feeling today?", ["Happy", "Sad", "Angry", "Excited", "Tired", "Neutral"])
trigger = st.text_input("🔍 What triggered this mood?")
submit = st.button("Save Mood")

if submit:
    if not trigger.strip():
        st.warning("⚠️ Please describe what triggered your mood.")
    else:
        mood_sheet = sheet.worksheet("Mood logs")
        mood_sheet.append_row([today, mood, trigger])
        st.success("✅ Mood successfully logged!")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🛠️ Day 8 | AniGPT v2 - Mood Logger with Google Sheet")
