import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LinearRegression
import calendar
from PIL import Image
from io import BytesIO
from openpyxl import load_workbook
import common

image = Image.open('for meta.png')
st.image(image,use_column_width=True)

image2 = Image.open('beta.png')
st.image(image2, width=80)
common.check_login()
st.warning("Meta 管理画面から落としたままの「Microsoft Excel 97-2003 ワークシート」はサポートしていません。  \n「Microsoft Excel ワークシート (.xlsx)」に変更の上アップロードしてください。")
st.info("ローデータファイルに必要な項目： レポート開始日, キャンペーン名,フリークエンシー,CPM,CTR(リンククリックスルー率),CPC(リンククリックの単価) (JPY)")

# グローバルでmatplotlib.pyplotを使用する際の警告を非表示にする
st.set_option('deprecation.showPyplotGlobalUse', False)

def plot_campaign_data(filtered_df,campaign_name, target_columns,selected_columns,end_date):
    # キャンペーン名と指定したカラムでフィルタリング
    campaign_df = filtered_df[(filtered_df["キャンペーン名"] == campaign_name) ]

    # レポート開始日列を日付型に変換
    campaign_df["レポート開始日"] = pd.to_datetime(campaign_df["レポート開始日"], format="%Y-%m-%d")

    # 終了日までの日数を計算
    end_date = pd.to_datetime(end_date)
    min_date = campaign_df["レポート開始日"].min()
    max_date = campaign_df["レポート開始日"].max()
    delta = abs((min_date - end_date).days)+1

    # 日数をインデックスに設定
    if delta < len(campaign_df):
        future_dates = pd.date_range(start=end_date, periods=delta+1, freq='D')
    else:
        future_dates = pd.date_range(start=min_date + pd.Timedelta(days=1), periods=delta+1, freq='D')
    future_df = pd.DataFrame({"レポート開始日": future_dates})

    # 予測レポート開始日分のデータを作成
    pred_data = pd.concat([campaign_df.loc[campaign_df["レポート開始日"] <= end_date], future_df])

    # 日数をインデックスに設定
    pred_data = pred_data.set_index("レポート開始日")


    # データを日別に集計
    daily_df = campaign_df.groupby([col for col in campaign_df.columns if col != "レポート開始日"]).mean()

    #  reset index to make it unique
    daily_df = daily_df.reset_index()

    # 予測対象レポート開始日の日付リストを作成
    min_date = pd.to_datetime(campaign_df["レポート開始日"].astype(str), format="%Y-%m-%d").min()

    # target_columnで指定された列のスライスを取得
    train_size = int(len(selected_columns) * 0.7)

    if end_date:
     if campaign_name and selected_columns:
         displayed_columns = set()
         for target_column in selected_columns:
          if target_column not in displayed_columns:
            displayed_columns.add(target_column)

     # データをトレーニング用とテスト用に分割
            campaign_df = campaign_df.sort_values(by="レポート開始日")
            train_data = filtered_df.loc[filtered_df["キャンペーン名"]==campaign_name].loc[:, ["レポート開始日"] + selected_columns].fillna(0)
            train_data = train_data.select_dtypes(include=[np.number])

     # 回帰分析モデルの作成と予測
            model = LinearRegression()
            model.fit(np.array(range(len(train_data))).reshape(-1, 1), train_data[target_column])
            future_range = np.array(range(len(train_data), len(train_data) + delta)).reshape(-1, 1)
            predictions = model.predict(future_range)[len(train_data):]
            predictions = np.maximum(predictions,0)


     # 予測結果をグラフで表示
            predicted_dates = pd.date_range(start=max_date + pd.Timedelta(days=1), periods=len(future_df), freq='D')

     # predicted_datesとpredictionsの長さを揃える
            if len(predicted_dates) > len(predictions):
                predicted_dates = predicted_dates[:len(predictions)]
            else:
                predictions = predictions[:len(predicted_dates)]

     # reset index to make it unique
            predicted_df = pd.DataFrame({"レポート開始日": predicted_dates, target_column: predictions}).reset_index(drop=True)

     # カラム名を変更
            predicted_df = predicted_df.rename(columns={"予測値": "レポート開始日"})


            if target_column == "CPM":
           # 実績値と予測値の合計を計算
             actual_sum = campaign_df[target_column].sum()
             pred_sum = predictions.sum()    
         # 実績値と予測値を合わせた平均値を計算
             merged_df = pd.concat([campaign_df, predicted_df])
             avg = merged_df[target_column].mean()
             st.write("","","")
             st.write("予想着地単価:￥ <b>{:,.2f}</b> N".format(avg), unsafe_allow_html=True)     

            elif target_column == "CPC(リンククリックの単価) (JPY)":
           # 実績値と予測値の合計を計算
             actual_sum = campaign_df[target_column].sum()
             pred_sum = predictions.sum()    
         # 実績値と予測値を合わせた平均値を計算
             merged_df = pd.concat([campaign_df, predicted_df])
             avg = merged_df[target_column].mean()
             st.write("","","")
             st.write("予想着地単価:￥<b>{:,.2f}</b> N".format(avg), unsafe_allow_html=True)    
             
            elif target_column == "フリークエンシー":
           # 実績値と予測値の合計を計算
             actual_sum = campaign_df[target_column].sum()
             pred_sum = predictions.sum()    
         # 実績値と予測値を合わせた平均値を計算
             merged_df = pd.concat([campaign_df, predicted_df])
             avg = merged_df[target_column].mean()
             st.write("","","")
             st.write("予想平均FQ:<b>{:,.2f}</b> ".format(avg), unsafe_allow_html=True)   


     # 両方のデータフレームを連結する
            merged_df = pd.concat([
            daily_df.assign(data_type="実績値"), 
            predicted_df.assign(data_type="予測値")], axis=0, ignore_index=True)
            merged_df = merged_df.reset_index().rename(columns={"index": "date"})

            chart = alt.Chart(merged_df).mark_bar(size=20).encode(
            x=alt.X("レポート開始日:T", title="日付", axis=alt.Axis(format="%m/%d")),
            y=alt.Y(target_column + ":Q", title=target_column),
            color=alt.Color("data_type:N", title="データ種別", scale=alt.Scale(domain=["実績値", "予測値"], range=["blue", "orange"]))
 ).properties(
            width=600,
            height=400,
            title=f"{target_column}の実績と予測"
 )
    
            st.altair_chart(chart, use_container_width=True)   


# ファイルのアップロード
uploaded_file = st.file_uploader("**ExcelまたはCSVファイルをアップロードしてください**", type=["xlsx", "csv"],help="必須項目：レポート開始日/キャンペーン名/フリークエンシー/CPM/リンククリック数/CPC/CTR/CPC")

if uploaded_file is not None:
    # データフレームの読み込み
    try:
        df = pd.read_excel(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file, engine='xlrd')
        
    try:
     df["レポート開始日"] = pd.to_datetime(df["レポート開始日"])
    
    except KeyError:
       st.error("ファイルの形式が異なります。")
       st.stop()
        
    except Exception as e:
     st.error("ファイルをもう一度確認してください")
     st.error(str(e))
     st.stop()
    # カラム名の指定
    target_columns = [
        "レポート開始日", "キャンペーン名","フリークエンシー","CPM",
        "CTR(リンククリックスルー率)","CPC(リンククリックの単価) (JPY)"
    ]

    # - を 0 に変換
    df = df.fillna(0)

    # 指定したカラム名が存在するかどうかをチェック
    if all(c in df.columns for c in target_columns):
        # 指定したカラム名と合致する列をフィルタリング
        filtered_df = df[target_columns]
    else:
        # 指定したカラム名が存在しない場合は空のデータフレームを作成
        filtered_df = pd.DataFrame(columns=target_columns)
        st.warning("必要な項目が不足しています。")

    dates = filtered_df["レポート開始日"].unique()

    campaign_name = st.selectbox("**キャンペーン名**", filtered_df["キャンペーン名"].unique())
    selected_columns = st.multiselect("**予測項目**", target_columns[2:])

    # 入力値を文字列として定義
    now = datetime.now()
    input_value = now.strftime('%Y-%m-%d')

    # 文字列をdatetimeオブジェクトに変換
    date_value = datetime.strptime(input_value, "%Y-%m-%d")

    col1, col2 = st.columns(2)

    # DateInputコンポーネントに渡す
    end_date = col1.date_input("**終了日を選択**", datetime.now(),help="レポートの終了日以後を選択ください。終了日が離れるほど、予測精度は悪化します。")
    
    if end_date:
     if campaign_name and selected_columns:
        for target_column in selected_columns:
            # グラフを描画
            plot_campaign_data(filtered_df,campaign_name, target_columns,selected_columns,end_date)
    else:
     st.warning("終了日を選択してください。")
