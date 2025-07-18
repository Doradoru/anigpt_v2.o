import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import altair as alt

st.set_page_config(page_title="AniGPT Dashboard", layout="wide")
st.title("📊 AniGPT – Personal Dashboard")

# ---------------------- Auth & Google Sheet Setup ----------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# ---------------------- User Selection ----------------------
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
user_lower = user.lower()

# ---------------------- Load Mood Logs Data ----------------------
worksheet = sheet.worksheet("Mood logs")
data = worksheet.get_all_records()
mood_df = pd.DataFrame(data)

# Fix column names to lowercase for safe access
mood_df.columns = [col.strip().lower() for col in mood_df.columns]

# Filter data by selected user
if "user" in mood_df.columns:
    filtered_df = mood_df[mood_df["user"].str.lower() == user_lower]
else:
    st.error("❌ 'User' column not found in Mood logs. Please check the sheet.")
    st.stop()

# ---------------------- Dashboard Display ----------------------
st.subheader(f"😊 Mood Logs for {user}")
if filtered_df.empty:
    st.info("No mood logs available yet.")
else:
    # Show latest 5 mood entries
    st.write("🕒 Last 5 Entries")
    st.dataframe(filtered_df.tail(5)[["date", "mood", "trigger"]].sort_values(by="date", ascending=False), use_container_width=True)

    # Pie chart of mood distribution
    mood_count = filtered_df["mood"].value_counts().reset_index()
    mood_count.columns = ["Mood", "Count"]

    st.write("📈 Mood Distribution")
    chart = alt.Chart(mood_count).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Mood", type="nominal"),
        tooltip=["Mood", "Count"]
    ).properties(width=400, height=400)

    st.altair_chart(chart, use_container_width=True)

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("Built by AniGPT v2.0 🔒 Private & Secure")
