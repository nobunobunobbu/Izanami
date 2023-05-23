import streamlit as st
from PIL import Image

image1 = Image.open('icon.png')
st.set_page_config(
    page_title="Izanami",page_icon=image1,
    layout="wide",
    initial_sidebar_state="auto", 
)

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


    tab1, tab2, tab3 = st.tabs(["Top", "ご意見・ご要望", "バージョン履歴"])

# with tab1:
    with tab1:
     st.header("TOP")
     st.write("機能説明")
     with st.expander('ポジネガ判定'):
         st.write("アップロードしたExcel ファイルの指定した列を行ごとに読み込み、各文章をポジ/ネガ/ニュートラルで判定します。")
     with st.expander('文章類似度測定'):
         st.write("アップロードした2つの文章を読み込み、その類似度を測定します。")
     with st.expander('未来予測forMeta'):
         st.markdown('アップロードしたローデータファイルを読み込み、各種指標の未来予測を指定日まで行います。  \n ※Meta管理画面から落としたファイル形式はサポートされていないので、Excel ワークブックに変更する必要があります。  \n  \n  推奨実績データ：14日間以上',unsafe_allow_html=True)
     with st.expander('未来予測forTwitter'):
         st.markdown('アップロードしたローデータファイルを読み込み、各種指標の未来予測を指定日まで行います。総予算を入力することで予想着地率も算出されます。  \n  \n 推奨実績データ：14日間以上',unsafe_allow_html=True)
     with st.expander('画像類似度測定'):
         st.write("アップロードした2つの画像を読み込み、その類似度を測定します。")


# with tab2:
    with tab2:
     st.write("""
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScdZ7GQtJbOq9keBHqWbfkEiUoo60vOmSZznBbwvq84NmV76A/viewform?embedded=true" 
            width="640" height="1108" frameborder="0" marginheight="0" marginwidth="0">
            読み込んでいます…
        </iframe>
    """, unsafe_allow_html=True)
    with tab3:
     st.header("Ver 1.00 (2023/05/22)")
     st.markdown('Izanami の以下機能をリリースしました。  \n・ポジネガ判定  \n・文章類似度測定  \n・未来予測forMeta β版  \n・未来予測forTwitter β版  \n ・画像類似度測定', unsafe_allow_html=True)

