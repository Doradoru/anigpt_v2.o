import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from secrets
json_data = st.secrets["GOOGLE_SHEET_JSON"]
creds_dict = json.loads(json_data)

# Auth
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# Open your sheet
sheet = client.open("AniGPT_DB")
st.success("Connected to AniGPT_DB ✅")
required_tabs = [
    "Memory", "Mood logs", "Daily journal", "Learning", "Reminders",
    "Life goals", "Voice logs", "Anibook outline", "Improvement notes",
    "Quotes", "User facts", "Task done", "Auto backup logs"
]

existing_tabs = [ws.title for ws in sheet.worksheets()]

for tab in required_tabs:
    if tab not in existing_tabs:
        sheet.add_worksheet(title=tab, rows=1000, cols=10)

st.success("✅ All required tabs are present or created.")
