# anigpt_v2.o/test_sheet_connection.py

import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Step 1: Scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Step 2: Load creds from secrets
creds = Credentials.from_service_account_info(
    st.secrets["GOOGLE_SHEET_JSON"],
    scopes=scope
)

# Step 3: Connect to sheet
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")  # Make sure spelling is correct

# Step 4: Try accessing sheet names
st.title("🧪 Google Sheet Connection Test")
st.success("✅ Connected to Google Sheet!")

st.write("Here are the available sheet tabs:")
tabs = [ws.title for ws in sheet.worksheets()]
st.write(tabs)

# Optional: Show data from "Users" tab
try:
    user_data = sheet.worksheet("Users").get_all_records()
    st.subheader("Users Sheet Preview:")
    st.write(user_data)
except Exception as e:
    st.error("❌ Couldn't read 'Users' sheet.")
    st.exception(e)
