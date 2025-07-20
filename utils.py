import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["GOOGLE_SHEET_JSON"], scopes=scope)
client = gspread.authorize(creds)

# Open the main Sheet
sheet = client.open("AniGPT_DB")

# Login Function
def login_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        users = worksheet.get_all_records()
        for user in users:
            if user.get("Name") == name and user.get("Password") == password:
                return True
        return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

# Register Function
def register_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        worksheet.append_row([name, password])
        return True
    except Exception as e:
        st.error(f"Registration error: {e}")
        return False
