import streamlit as st
from PIL import Image

image = Image.open('IZANAMI.png')
st.image(image, use_column_width=True)

def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            st.session_state["logged_in"] = True  # set logged_in to True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            if "logged_in" in st.session_state:
                del st.session_state["logged_in"]  # remove logged_in if password incorrect

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.session_state["username"] = st.text_input("ログインID", help="Enter/Tab キーによる切り替えは無効です")
        st.session_state["password"] = st.text_input(
            "パスワード", type="password"
        )
        if st.button("ログイン"):
            password_entered()
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.session_state["username"] = st.text_input("Username")
        st.session_state["password"] = st.text_input(
            "Password", type="password"
        )
        if st.button("ログイン"):
            password_entered()
        st.error("😕 ユーザーID かパスワードが異なります")
        return False
    else:
        # Password correct.
        return True

if check_password():

    tab1, tab2, tab3 = st.tabs(["Top", "ご意見・ご要望", "バージョン履歴"])

# with tab1:
    with tab1:
     st.header("TOP")
     st.write('Comming Soon!')

# with tab2:
    with tab2:
     st.write("""
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScdZ7GQtJbOq9keBHqWbfkEiUoo60vOmSZznBbwvq84NmV76A/viewform?embedded=true" 
            width="640" height="1108" frameborder="0" marginheight="0" marginwidth="0">
            読み込んでいます…
        </iframe>
    """, unsafe_allow_html=True)
    with tab3:
     st.header("Ver 1.00")
     st.write('Izanami をリリースしました。')
