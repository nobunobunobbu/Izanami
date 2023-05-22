import streamlit as st
import pandas as pd
import re
import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from janome.tokenizer import Tokenizer
from PIL import Image
import common

image = Image.open('IZANAMI.png')

common.check_login()

st.image(image,use_column_width=True)
st.title('ポジネガ判定')


# BERTモデルとトークナイザの読み込み
model_name = "christian-phu/bert-finetuned-japanese-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)



# Excelファイルのアップロード
uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xls", "xlsx"])

if uploaded_file is not None:
    # Excelデータの読み込み
    df = pd.read_excel(uploaded_file)

    # テキスト列の選択
    text_column = st.selectbox("テキスト列を選択してください", df.columns)

    # 判定結果のカウント用変数
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    # max_lengthの指定
    max_length = 80

    # 判定開始ボタン
    if st.button("判定開始"):
        # アナウンスの表示

        # 空白行までの行数を取得
        null_indices = df[df[text_column].isnull()].index
        num_rows = null_indices[0] if len(null_indices) > 0 else df.shape[0]
        df = df.iloc[:num_rows]

        # 行番号と進捗バーの表示
        progress_bar = st.progress(0)
        current_row = st.empty()

        predictions = []

        # テキストのポジティブ・ニュートラル・ネガティブ判定
        for i, row in df.iterrows():
            text = str(row[text_column])

            current_row.text(f"処理中: {i+1}/{num_rows} 行")
            progress_bar.progress((i+1) / num_rows)

            # リンクの除外
            text_without_links = re.sub(r'http\S+', '', text)
            
            # 形態素解析
            janome_tokenizer = Tokenizer()
            text_tokens = [token.surface for token in janome_tokenizer.tokenize(text_without_links)]

            # テキストの長さを制限
            if len(text_tokens) > max_length:
                text_tokens = text_tokens[:max_length]

            # パディング
            if len(text_tokens) < max_length:
                text_tokens += [''] * (max_length - len(text_tokens))

            # 文字列に戻す
            input_text = ' '.join(text_tokens)

            # トークン化とエンコード
            inputs = tokenizer.encode_plus(
                input_text,
                add_special_tokens=True,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=max_length
            )

            with torch.no_grad():
                outputs = model(**inputs).logits


            predicted_label = torch.argmax(outputs, dim=1).item()

            # 判定結果のカウント
            if predicted_label == 0:
                negative_count += 1
                predictions.append("ネガティブ")
            elif predicted_label == 1:
                neutral_count += 1
                predictions.append("ニュートラル")
            elif predicted_label == 2:
                positive_count += 1
                predictions.append("ポジティブ")

        # 結果の表示
        st.write("ポジティブ: ", positive_count)
        st.write("ニュートラル: ", neutral_count)
        st.write("ネガティブ: ", negative_count)

        # 円グラフの作成
        labels = ['ポジティブ', 'ニュートラル', 'ネガティブ']
        values = [positive_count, neutral_count, negative_count]
        colors = ['blue', 'lightgrey', 'red']

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
        fig.update_layout(title='判定結果の割合')

        # 円グラフをStreamlit上で表示
        st.plotly_chart(fig)

        # 選択した列の各行の判定結果を出力
        df["判定結果"] = predictions
        st.write("判定結果:")
        st.dataframe(df[[text_column, "判定結果"]])
