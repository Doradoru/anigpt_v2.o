import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Page settings
st.set_page_config(page_title="AniGPT", page_icon="🧠")

st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")

# Get credentials from secrets.toml
json_key = st.secrets["GOOGLE_SHEET_JSON"]
credentials_dict = json.loads(json_key)

# Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# Sheet and user info
sheet = client.open("AniGPT_DB")
user = st.text_input("👤 Your Name (e.g. Ani, Anne)", max_chars=30)

tab_options = [
    "Mood logs", "Daily journal", "Learning", "Reminders", "Life goals", "Quotes", "Task done"
]
selected_tab = st.selectbox("📂 Where to save this input?", tab_options)

user_input = st.text_area("✍️ Your Input (thoughts, notes, learning...)", height=150)
submit = st.button("💾 Save to Google Sheet")


import streamlit as st
st.title("🔐 AniGPT Secret Test")

try:
    secret_json = st.secrets["GOOGLE_SHEET_JSON"]
    st.success("✅ Secret Loaded Successfully!")
    st.code(secret_json)
except KeyError as e:
    st.error(f"❌ Secret not found: {e}")
