if submitted:
    success = login_user(uname.strip(), upass.strip())  # Add strip() to clean input
    if success:
        st.success(f"Welcome back, {uname} ✅")
        st.session_state["user"] = uname
    else:
        st.error("Invalid username or password ❌")
