import streamlit as st
from PIL import Image
import openai
from streamlit_chat import message

image1 = Image.open('icon.png')
st.set_page_config(
    page_title="Izanami",page_icon=image1,
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
        st.session_state["username"] = st.text_input("ログインID")
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
    tab1, tab2, tab3 , tab4 = st.tabs(["チャット機能","機能説明", "ご意見・ご要望", "バージョン履歴"])

# with tab1:
    with tab2:
     st.write("機能説明")
     with st.expander('PDF 要約機能'):
         st.write("アップロードしたPDF ファイルを読み込み、ChatGPT を用いてわかりやすく解説します。 ")
     with st.expander('クリエイティブサポート'):
         st.write("Twitter・Instagram 用の投稿文を作成します。  \n 画像生成機能を実装しました。  \n また、薬機法・景表法判定もサポートしています。テキストまたは画像内のテキストを読み込んで判定可能です。 ")
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



    with tab3:
     st.write("""
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScdZ7GQtJbOq9keBHqWbfkEiUoo60vOmSZznBbwvq84NmV76A/viewform?embedded=true" 
            width="640" height="1108" frameborder="0" marginheight="0" marginwidth="0">
            読み込んでいます…
        </iframe>
    """, unsafe_allow_html=True)
    with tab4:
     with st.expander("Ver 1.31 (2023/06/16)"):
      st.markdown('要約機能を強化しました。  \n・音声文字起こし・要約機能の追加。', unsafe_allow_html=True)
     with st.expander("Ver 1.22 (2023/06/15)"):
      st.markdown('クリエイティブサポート機能を強化しました。  \n・より長文のプロンプトを受け付けるgpt-3.5-turbo-16k に対応。  \n ・テキストファイルダウンロードに対応。  \n PDF 要約機能を強化しました。  \n ・word ファイルの出力に対応。', unsafe_allow_html=True)
     with st.expander("Ver 1.21 (2023/06/06)"):
      st.markdown('クリエイティブサポート機能を強化しました。  \n・画像生成機能を追加。webページ読み込みに対応  \n・投稿文作成でwebページ読み込みに対応', unsafe_allow_html=True)
     with st.expander("Ver 1.20 (2023/06/02)"):
      st.markdown('Izanami の以下機能をリリースしました。  \n・クリエイティブサポート', unsafe_allow_html=True)
     with st.expander("Ver 1.11 (2023/05/26)"):
      st.markdown('未来予測forTwitter ・未来予測forMeta の予測期間の不具合を修正。  \n 必要項目のインフォメーションを追加。', unsafe_allow_html=True)
     with st.expander("Ver 1.10 (2023/05/24)"):
      st.markdown('Izanami の以下機能をリリースしました。  \n・PDF 要約機能', unsafe_allow_html=True)
     with st.expander("Ver 1.00 (2023/05/23)"):
      st.markdown('Izanami の以下機能をリリースしました。  \n・ポジネガ判定  \n・文章類似度測定  \n・未来予測forMeta β版  \n・未来予測forTwitter β版  \n ・画像類似度測定', unsafe_allow_html=True)

    with tab1:
 # ChatGPT のAPIキー入力用テキストボックス
     api_key = st.secrets["api_key"]["api_key"]
     st.session_state.api_key = api_key

     st.title("💬 ChatGPT")
#openai.api_key = st.secrets.openai_api_key
     if "messages" not in st.session_state:
      st.session_state["messages"] = [{"role": "assistant", "content": "何かお困りですか？"}]

     with st.form("chat_input", clear_on_submit=True):
      a, b = st.columns([4, 1])
      user_input = a.text_input(
        label="Your message:",
        placeholder="ChatGPT に訊きたいことを入力",
        label_visibility="collapsed",
    )
      b.form_submit_button("送信", use_container_width=True)

     for msg in st.session_state.messages:
      message(msg["content"], is_user=msg["role"] == "user")

     if user_input and not api_key:
       st.info("Please add your OpenAI API key to continue.")
    
     if user_input and api_key:
       openai.api_key = api_key
       st.session_state.messages.append({"role": "user", "content": user_input})
       message(user_input, is_user=True)
       response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
       msg = response.choices[0].message
       st.session_state.messages.append(msg)
       message(msg.content)
