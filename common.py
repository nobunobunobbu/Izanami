
# common.py
import streamlit as st
import extra_streamlit_components as stx

#ログインの確認
def check_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("**ログインしてください**")
        st.stop()