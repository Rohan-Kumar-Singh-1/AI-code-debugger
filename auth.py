import streamlit as st
from database import create_user, authenticate_user


def login_page():

    st.title("🔐 Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = authenticate_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.user_id = user["id"]
                st.rerun()

            else:
                st.error("Invalid credentials")


    with tab2:

        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):

            success = create_user(new_user, new_pass)

            if success:
                st.success("User created! You can login now.")

            else:
                st.error("Username already exists")