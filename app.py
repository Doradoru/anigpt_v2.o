import streamlit as st
from utils import register_user, login_user

st.set_page_config(page_title="AniGPT Login", layout="centered")
st.title("🔐 AniGPT Login System")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Login / Register form
tab1, tab2 = st.tabs(["🔓 Login", "🆕 Register"])

with tab1:
    st.subheader("Login to AniGPT")
    uname = st.text_input("Name")
    upass = st.text_input("Password", type="password")
    if st.button("Login"):
        success = login_user(uname, upass)
        if success:
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.username = uname
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

with tab2:
    st.subheader("Create New Account")
    new_name = st.text_input("New Name")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Register"):
        created, msg = register_user(new_name, new_pass)
        if created:
            st.success("✅ " + msg)
        else:
            st.error("❌ " + msg)

# After login
if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.username} 👋")
    st.page_link("app_main.py", label="➡️ Go to AniGPT Dashboard", icon="🧠")
