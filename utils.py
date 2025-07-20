# utils.py

import gspread
import json
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

# Define scope
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from secrets.toml
creds_dict = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# ✅ Login Function
def login_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        records = worksheet.get_all_records()
        for user in records:
            if user["Name"] == name and user["Password"] == password:
                return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

# ✅ Optional: New User Register Function (future use)
def register_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        worksheet.append_row([name, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        return True
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False
