import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from PIL import Image

image = Image.open('IZANAMI.png')

st.image(image,use_column_width=True)

def get_cosine_sim(text1, text2):
    # CountVectorizerを使用して、テキストのベクトル表現を作成します。
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    # コサイン類似度を計算します。
    cosine_sim = cosine_similarity(vectorizer)
    return cosine_sim[0][1]

def main():
    st.title("文章類似度測定")
    st.write("テキストを入力してください。")

    # テキストボックスから文章を取得します。
    text1 = st.text_area("テキスト1", "")
    text2 = st.text_area("テキスト2", "")

    if st.button("測定"):
        # コサイン類似度を計算します。
        cosine_sim = get_cosine_sim(text1, text2)
        # 結果を表示します。
        st.write("類似度：{}%".format(round(cosine_sim*100, 2)))

if __name__ == '__main__':
    main()
