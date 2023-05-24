import streamlit as st
from PyPDF2 import PdfReader
import requests
import textwrap
from PIL import Image

image = Image.open('IZANAMI.png')

st.image(image,use_column_width=True)

# Streamlit アプリケーションの設定
st.title("Summarize PDF with ChatGPT")

# ChatGPT のAPIキー入力用テキストボックス
api_key = st.text_input("ChatGPT のAPI Key を入力してください", type="password")
st.session_state.api_key = api_key

# ユーザーからPDF ファイルをアップロード
uploaded_file = st.file_uploader("PDF ファイルをアップロードしてください", type="pdf")

# モデル選択のセレクトボックス
model = st.selectbox('GPTモデルの選択', ['gpt-3.5-turbo', 'gpt-4'],help="GPT4 での実行はChatGPT Plus への加入が必要です")

# 実行ボタン
run_button = st.button('実行')

if run_button:
    if uploaded_file is not None and api_key != "":
        # アップロードされたPDF ファイルを解析してテキストを抽出
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    # テキストをトークン数に合わせて分割
    chunks = textwrap.wrap(text, 2000)

    explanations = []

    for chunk in chunks:
        # ChatGPT にテキストを送信して解説を生成
        prompt = "テキストを読んで内容をマークダウンでわかりやすく解説して"
        headers = {
            "Authorization": f"Bearer {st.session_state.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt + chunk
                }
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            try:
                explanation = response.json()["choices"][0]["message"]["content"].strip()
                explanations.append(explanation)
            except KeyError:
                st.error("Failed to retrieve explanation from the API response.")
        else:
            try:
                error_details = response.json()
            except ValueError:
                error_details = "No additional information."
            st.error(f"API request failed with status code: {response.status_code}. Details: {error_details}")

    # All explanations are displayed as a single text
    st.subheader("▼")
    st.write(' '.join(explanations))
