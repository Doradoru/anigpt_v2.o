import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]

    creds_dict = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("AniGPT_DB")
    return sheet

def register_user(name, password):
    sheet = connect_to_sheet()
    users_tab = sheet.worksheet("Users")
    existing = users_tab.col_values(1)
    
    if name in existing:
        return False, "Username already exists."
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_tab.append_row([name, password, now])
    return True, "Account created successfully!"

def login_user(name, password):
    sheet = connect_to_sheet()
    users_tab = sheet.worksheet("Users")
    data = users_tab.get_all_records()
    for user in data:
        if user['Name'] == name and user['Password'] == password:
            return True
    return False
