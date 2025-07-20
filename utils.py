import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Set the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from secrets.toml
creds = Credentials.from_service_account_info(st.secrets["GOOGLE_SHEET_JSON"], scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

def login_user(name, password):
    try:
        users_tab = sheet.worksheet("Users")
        users = users_tab.get_all_records()
        for user in users:
            if user['Name'] == name and user['Password'] == password:
                return True
        return False
    except Exception as e:
        st.error(f"Login Error: {e}")
        return False

def register_user(name, password):
    try:
        users_tab = sheet.worksheet("Users")
        users_tab.append_row([name, password])
        return True
    except Exception as e:
        st.error(f"Register Error: {e}")
        return False
