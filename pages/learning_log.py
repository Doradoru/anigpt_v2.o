import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

st.set_page_config(page_title="📚 Learning Log", layout="centered")

st.title("📚 Log Your Learnings")

# Load credentials from Streamlit secrets
json_key = st.secrets["GOOGLE_SHEET_JSON"]
if isinstance(json_key, str):
    json_key = json.loads(json_key)

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")
worksheet = sheet.worksheet("Learning")

# Learning form
with st.form("learning_form"):
    learning = st.text_area("🧠 What did you learn today?", placeholder="e.g. Streamlit basics, pandas syntax...")
    context = st.text_input("📌 Context or Source", placeholder="e.g. YouTube video, ChatGPT, book name...")
    user = st.selectbox("👤 Who is learning?", ["Ani", "Anne"])
    submitted = st.form_submit_button("💾 Save")

    if submitted:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        worksheet.append_row([date, learning, context, user])
        st.success("✅ Learning saved successfully!")
