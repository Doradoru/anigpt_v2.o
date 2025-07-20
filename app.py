import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT Login", layout="centered")
st.title("🔐 AniGPT Login System")

menu = ["Login", "Register"]
choice = st.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to AniGPT")
    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(uname, upass):
            st.success(f"Welcome, {uname} 🎉")
            st.info("You're now logged in to AniGPT.")
        else:
            st.error("Invalid credentials ❌")

elif choice == "Register":
    st.subheader("Register New User")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')
    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account created successfully 🎉 You can now log in.")
        else:
            st.error("Something went wrong during registration ❌")
