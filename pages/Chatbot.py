import openai
import streamlit as st
from PIL import Image
import common

image = Image.open('IZANAMI.png')

st.image(image,use_column_width=True)

common.check_login()

# ChatGPTのAPIキーを取得
api_key = st.secrets["api_key"]["api_key"]
st.session_state.api_key = api_key

st.title("💬 Chatbot")
model_choice = st.selectbox('モデルの選択', ['gpt-3.5-turbo', 'gpt-4-1106-preview'])
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "何かお困りですか？"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    openai.api_key = st.session_state.api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model=model_choice, messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
