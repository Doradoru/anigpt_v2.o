from utils import login_user

uname = st.text_input("Username")
upass = st.text_input("Password", type="password")

if st.button("Login"):
    if login_user(uname, upass):
        st.success(f"Welcome {uname}!")
    else:
        st.error("Invalid credentials ❌")
