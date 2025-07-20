import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import json
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# For Streamlit secrets.toml
creds_dict = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")
