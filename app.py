# app.py
import streamlit as st
from utils import login_user
from datetime import datetime

st.set_page_config(page_title="AniGPT Login", page_icon="🤖")

st.title("🔐 AniGPT Login")

with st.form("login_form"):
    uname = st.text_input("Username")
    upass = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    success = login_user(uname, upass)
    if success:
        st.success(f"Welcome back, {uname}! ✅")
        st.session_state["user"] = uname
        st.switch_page("dashboard.py")  # Optional: If you use multipage
    else:
        st.error("Invalid username or password ❌")
