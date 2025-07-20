# utils.py

import gspread
import streamlit as st
import json
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Use Streamlit secrets for credentials
creds_dict = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

def login_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        records = worksheet.get_all_records()
        for user in records:
            if user['Name'] == name and user['Password'] == password:
                return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False
