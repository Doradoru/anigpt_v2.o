import streamlit as st
from utils import login_user, register_user

st.title("🔐 AniGPT Login")

menu = ["Login", "Sign Up"]
choice = st.selectbox("Select Action", menu)

if choice == "Login":
    st.subheader("Login to AniGPT")
    uname = st.text_input("Username")
    upass = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(uname.strip(), upass.strip()):
            st.success(f"✅ Welcome {uname}")
            st.session_state["user"] = uname
        else:
            st.error("❌ Invalid username or password")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Create Account"):
        if register_user(new_user.strip(), new_pass.strip()):
            st.success("✅ Account created successfully. Now you can login.")
        else:
            st.error("⚠️ Something went wrong. Try again.")
