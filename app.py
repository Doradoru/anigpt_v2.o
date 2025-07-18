import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="🧠 AniGPT Input", layout="centered")
st.title("📥 AniGPT: Smart Auto Input Panel")

# ✅ Get user from URL
query_params = st.experimental_get_query_params()
user = query_params.get("user", ["Unknown"])[0]  # Default to Unknown

if user not in ["Ani", "Anne"]:
    st.warning("🚫 Invalid or missing user. Please use a link with `?user=Ani` or `?user=Anne`")
    st.stop()

# 🔐 Credentials
json_key = st.secrets["GOOGLE_SHEET_JSON"]
if isinstance(json_key, str):
    json_key = json.loads(json_key)
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# 🔗 Sheet open
SHEET_URL = "https://docs.google.com/spreadsheets/d/1UIYuoQRhRfR1rjoy-6jHK5tLyCso-3fBvqLtSTv3-lc"
sheet = client.open_by_url(SHEET_URL)

# 🔍 Detect Tab Automatically (Optional: via route or page name)
tab = st.selectbox("📑 Select Entry Type", ["Mood logs", "Daily journal", "Reminders", "Learning", "Quotes"])

# 📝 Input
data = {}
if tab == "Mood logs":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Mood"] = st.selectbox("How do you feel?", ["😊 Happy", "😞 Sad", "😠 Angry", "😐 Neutral"])
    data["Trigger"] = st.text_input("What triggered this mood?")
    data["User"] = user

elif tab == "Daily journal":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Summary"] = st.text_area("What happened today?")
    data["Keywords"] = st.text_input("Keywords (comma-separated)")
    data["User"] = user

elif tab == "Reminders":
    data["Task"] = st.text_input("Reminder Task")
    data["Date"] = st.date_input("Reminder Date")
    data["Time"] = st.time_input("Reminder Time")
    data["Status"] = "Pending"
    data["User"] = user

elif tab == "Learning":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["WhatWasLearned"] = st.text_area("What did you learn?")
    data["Context"] = st.text_input("Context or Example")
    data["User"] = user

elif tab == "Quotes":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Quote"] = st.text_area("Enter the quote")
    data["Source"] = st.text_input("Quote Source")
    data["User"] = user

# ✅ Submit Button
if st.button("💾 Auto-Save Entry"):
    try:
        ws = sheet.worksheet(tab)
        headers = ws.row_values(1)
        row = [data.get(h, "") for h in headers]
        ws.append_row(row)
        st.success(f"✅ Entry saved successfully to {tab} as {user}")
    except Exception as e:
        st.error(f"❌ Failed to save entry.\n\n{e}")
