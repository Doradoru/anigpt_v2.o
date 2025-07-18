import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import altair as alt

st.set_page_config(page_title="AniGPT Dashboard", layout="wide")
st.title("📊 AniGPT – Personal Dashboard")

# ---------------------- Google Sheets Auth ----------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# ---------------------- User Selection ----------------------
user = st.selectbox("👤 Select User", ["Ani", "Anne"])
user_lower = user.lower()

# ---------------------- Mood Logs Data Load ----------------------
worksheet = sheet.worksheet("Mood logs")
data = worksheet.get_all_records()
mood_df = pd.DataFrame(data)

# Normalize column names
mood_df.columns = [col.strip().lower() for col in mood_df.columns]

# ---------------------- Auto-Fix: Add 'User' Column if Missing ----------------------
if 'user' not in mood_df.columns:
    st.warning("⚠️ 'User' column missing! Auto-adding now...")

    # Get full values from sheet (not just records)
    values = worksheet.get_all_values()
    headers = values[0]

    if "User" not in headers:
        headers.append("User")
        for i in range(1, len(values)):
            values[i].append("Ani")  # default user value

        worksheet.update("A1", values)
        st.success("✅ 'User' column added to Mood logs tab.")

        # Reload updated data
        data = worksheet.get_all_records()
        mood_df = pd.DataFrame(data)
        mood_df.columns = [col.strip().lower() for col in mood_df.columns]

# ---------------------- Filter by User ----------------------
filtered_df = mood_df[mood_df["user"].str.lower() == user_lower]

# ---------------------- Dashboard Output ----------------------
st.subheader(f"😊 Mood Logs for {user}")
if filtered_df.empty:
    st.info("No mood logs found for this user.")
else:
    st.write("🕒 Last 5 Entries")
    st.dataframe(
        filtered_df.tail(5)[["date", "mood", "trigger"]].sort_values(by="date", ascending=False),
        use_container_width=True
    )

    st.write("📈 Mood Distribution")
    mood_count = filtered_df["mood"].value_counts().reset_index()
    mood_count.columns = ["Mood", "Count"]

    chart = alt.Chart(mood_count).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Mood", type="nominal"),
        tooltip=["Mood", "Count"]
    ).properties(width=400, height=400)

    st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ by AniGPT v2.0")
