import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# --- Ensure 'Users' Tab ---
def ensure_users_tab():
    try:
        ws = sheet.worksheet("Users")
        headers = ws.row_values(1)
        required = ["Name", "Password", "Created At"]
        if headers != required:
            ws.clear()
            ws.append_row(required)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title="Users", rows=100, cols=3)
        ws.append_row(["Name", "Password", "Created At"])

ensure_users_tab()

# --- Login Function ---
def login_user(name, password):
    ws = sheet.worksheet("Users")
    users = ws.get_all_records()
    for user in users:
        if "Name" in user and "Password" in user:
            if user["Name"] == name and user["Password"] == password:
                return True
    return False

# --- Optional: Signup Function ---
def signup_user(name, password):
    ws = sheet.worksheet("Users")
    ws.append_row([name, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    return True
