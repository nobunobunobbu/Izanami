import streamlit as st
import io
import numpy as np
import hashlib
from PIL import Image


image = Image.open('IZANAMI.png')

st.image(image,use_column_width=True)

def main():
    st.title('画像類似度測定')
    st.write('画像をアップロードしてください。')

    # 2つのファイルをアップロードする
    uploaded_file1 = st.file_uploader("画像1", type=['png', 'jpg'])
    uploaded_file2 = st.file_uploader("画像2", type=['png', 'jpg'])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        # 画像を読み込む
        image1 = Image.open(uploaded_file1)
        image2 = Image.open(uploaded_file2)

        # 画像の表示
        st.image([image1, image2], caption=['Image 1', 'Image 2'], width=300)

        if st.button('測定'):
            # ハミング距離の計算
            image1_hash = hashlib.md5(np.array(image1)).hexdigest()
            image2_hash = hashlib.md5(np.array(image2)).hexdigest()
            hamming_distance = sum(c1 != c2 for c1, c2 in zip(image1_hash, image2_hash))
            similarity = (len(image1_hash) - hamming_distance) / len(image1_hash) * 100

            # 結果の表示
            st.write(f'類似度: {similarity}%')

if __name__ == '__main__':
    main()
