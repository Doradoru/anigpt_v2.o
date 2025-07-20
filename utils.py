import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

sheet = client.open("AniGPT_DB")

def login_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        records = worksheet.get_all_records()
        for user in records:
            if user["Name"] == name and user["Password"] == password:
                return True
        return False
    except Exception as e:
        return False

def register_user(name, password):
    try:
        worksheet = sheet.worksheet("Users")
        worksheet.append_row([name, password, str(datetime.now())])
        return True
    except Exception as e:
        return False
