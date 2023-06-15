import streamlit as st
from PyPDF2 import PdfReader
import requests
import textwrap
from PIL import Image
import common
from datetime import datetime

image = Image.open('IZANAMI.png')

st.image(image,use_column_width=True)

common.check_login()

# Streamlit アプリケーションの設定
st.title("PDF 要約機能")

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")

# ChatGPT のAPIキー入力用テキストボックス
api_key = st.secrets["api_key"]["api_key"]
st.session_state.api_key = api_key

# ユーザーからPDF ファイルをアップロード
uploaded_file = st.file_uploader("PDF ファイルをアップロードしてください", type="pdf")

# モデル選択のセレクトボックス
model = st.selectbox('GPTモデルの選択', ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4'],help="gpt-3.5-turbo-16k :より長文のプロンプトを受け付けます。gpt-4:未対応となります。")

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
    with open('answer.txt', 'w',encoding='UTF-8') as f:
                 f.write(' '.join(explanations))
                st.download_button(
                label="ダウンロード",
                data=open('answer.txt', 'rb'),
                file_name= date_str +"_"+PDF要約.txt',
                mime='text/plain',
            )

