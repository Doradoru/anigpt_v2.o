import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

st.set_page_config(page_title="AniGPT v2.0", layout="centered")

st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")
st.markdown("Start chatting, journaling, or saving your thoughts. Your twin AI is listening...")

# Load credentials securely from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]  # Make sure this exists in secrets.toml
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("AniGPT_DB")

# Auto-create required tabs if not present
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "
