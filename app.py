import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json

# 🎯 Page Config
st.set_page_config(page_title="AniGPT Input", layout="centered")
st.title("🧠 AniGPT: Auto Smart Entry Panel")

# 🔐 Load secrets
json_key = st.secrets["GOOGLE_SHEET_JSON"]
if isinstance(json_key, str):
    json_key = json.loads(json_key)

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# 📎 Open Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1UIYuoQRhRfR1rjoy-6jHK5tLyCso-3fBvqLtSTv3-lc"
sheet = client.open_by_url(SHEET_URL)

# ✅ Select User
user = st.selectbox("👤 Select User", ["Ani", "Anne"])

# ✅ Select Entry Type (internally)
entry_type = st.radio("📝 What would you like to log?", [
    "Mood logs",
    "Daily journal",
    "Reminders",
    "Learning",
    "Quotes"
])

# 🔄 Auto Form Fields Based on Entry Type
data = {"User": user}
if entry_type == "Mood logs":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Mood"] = st.selectbox("Mood", ["😊 Happy", "😞 Sad", "😠 Angry", "😐 Neutral"])
    data["Trigger"] = st.text_input("Trigger")

elif entry_type == "Daily journal":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Summary"] = st.text_area("Summary of the day")
    data["Keywords"] = st.text_input("Keywords")

elif entry_type == "Reminders":
    data["Task"] = st.text_input("Task")
    data["Date"] = st.date_input("Date")
    data["Time"] = st.time_input("Time")
    data["Status"] = "Pending"

elif entry_type == "Learning":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["WhatWasLearned"] = st.text_area("What did you learn?")
    data["Context"] = st.text_input("Context or Example")

elif entry_type == "Quotes":
    data["Date"] = datetime.today().strftime("%Y-%m-%d")
    data["Quote"] = st.text_area("Enter the quote")
    data["Source"] = st.text_input("Quote Source")

# ✅ Auto-create tab if missing + auto-add User column if needed
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

# ✅ Save Button
if st.button("💾 Save Entry"):
    try:
        ws, headers = ensure_tab_and_columns(entry_type, data)
        row = [data.get(h, "") for h in headers]
        ws.append_row(row)
        st.success(f"✅ Entry saved to '{entry_type}' for {user}")
    except Exception as e:
        st.error(f"❌ Error saving: {e}")
