import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime

st.set_page_config(page_title="AniGPT v2.0", layout="centered")
st.title("🧠 AniGPT v2.0 – Your Personal Learning Assistant")
st.markdown("Start journaling, saving thoughts, or giving commands. Your AI twin is listening...")

# Load credentials securely from secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client
