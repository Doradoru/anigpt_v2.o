import streamlit as st
from utils import login_user, register_user

st.title("🔐 AniGPT Login System")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")

    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')

    if st.button("Login"):
        if login_user(uname, upass):
            st.success(f"Welcome {uname} 🎉")
        else:
            st.error("Login Failed ❌")

elif choice == "Register":
    st.subheader("Create New Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')

    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account Created Successfully 🎉")
        else:
            st.error("Registration Failed ❌")
