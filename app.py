import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT Login", layout="centered")
st.title("🔐 AniGPT Login System")

menu = ["Login", "Register"]
choice = st.selectbox("Select Action", menu)

if choice == "Login":
    st.subheader("Login to AniGPT")
    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(uname, upass):
            st.success(f"Welcome {uname}!")
        else:
            st.error("Incorrect username or password ❌")

elif choice == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')
    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("User registered successfully 🎉")
        else:
            st.error("Failed to register user ❌")
