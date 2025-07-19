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
