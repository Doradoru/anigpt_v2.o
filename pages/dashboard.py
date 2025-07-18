import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import altair as alt

st.set_page_config(page_title="AniGPT Dashboard", layout="wide")
st.title("📊 AniGPT Dashboard – Personal Insights")

# Auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_key = st.secrets["GOOGLE_SHEET_JSON"]
service_account_info = json.loads(json_key)
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# User selector
user = st.selectbox("👤 Select user", ["Ani", "Anne"])

# Load mood logs
def load_tab(tab_name):
    try:
        worksheet = sheet.worksheet(tab_name)
        data = worksheet.get_all_values()
        headers = data[0]
        df = pd.DataFrame(data[1:], columns=headers)
        return df
    except:
        return pd.DataFrame()

# ---------- MOOD ANALYSIS ----------
st.subheader("💖 Mood Analysis")
mood_df = load_tab("Mood logs")
if not mood_df.empty:
    mood_df = mood_df[mood_df['User'] == user]
    mood_counts = mood_df['Mood'].value_counts().reset_index()
    mood_counts.columns = ['Mood', 'Count']
    chart = alt.Chart(mood_counts).mark_bar().encode(
        x='Mood',
        y='Count',
        color='Mood'
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No mood logs found.")

# ---------- LEARNING SUMMARY ----------
st.subheader("📘 Learning Summary")
learn_df = load_tab("Learning")
if not learn_df.empty:
    learn_df = learn_df[learn_df['Context'] == user]
    st.write(f"🧠 Total Learnings by {user}: {len(learn_df)}")
    st.dataframe(learn_df.tail(5))
else:
    st.info("No learnings found.")

# ---------- REMINDERS ----------
st.subheader("🗓️ Task Progress")
reminder_df = load_tab("Reminders")
if not reminder_df.empty:
    user_tasks = reminder_df[reminder_df['Status'] == 'pending']
    st.write(f"⏳ Pending Tasks for {user}: {len(user_tasks)}")
    st.dataframe(user_tasks.tail(5))
else:
    st.info("No reminders found.")

# ---------- LIFE GOALS ----------
st.subheader("🎯 Life Goals")
goals_df = load_tab("Life goals")
if not goals_df.empty:
    goals_df = goals_df[goals_df['Progress'].str.endswith('%')]
    goals_df['Progress'] = goals_df['Progress'].str.replace('%', '').astype(int)
    for i, row in goals_df.iterrows():
        st.text(f"🎯 {row['Goal']} ({row['Category']})")
        st.progress(row['Progress'] / 100)
else:
    st.info("No goals found.")

# ---------- JOURNAL ----------
st.subheader("📓 Recent Journal Entries")
journal_df = load_tab("Daily journal")
if not journal_df.empty:
    journal_df = journal_df.tail(5)
    st.table(journal_df)
else:
    st.info("No journal entries found.")

