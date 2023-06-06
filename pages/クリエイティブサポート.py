import streamlit as st
import requests
import textwrap
from PIL import Image
import easyocr
import numpy as np
import common
import requests

image = Image.open('IZANAMI.png')


st.image(image,use_column_width=True)
common.check_login()

# Streamlit アプリケーションの設定
st.title("クリエイティブサポート")

tab1, tab2,tab3 = st.tabs(["投稿文作成","画像生成","薬機法/景表法判定"])

with tab1:
 # ChatGPT のAPIキー入力用テキストボックス
 api_key = st.secrets["api_key"]["api_key"]
 st.session_state.api_key = api_key

 # ユーザーからの質問をテキストボックスで受け取る
 promotion = st.text_input("商材名")
 content_gen = st.selectbox('コンテンツ生成方法', ['テキストから生成', 'リンクから生成'])

 if content_gen == 'テキストから生成':
  question = st.text_area("商材の特長")

  col1, col2 = st.columns(2)

  youso = col1.text_area("入れ込みたい要素①")
  youso1 = col2.text_area("入れ込みたい要素②")

  col3, col4,col5 = st.columns(3)
  youso2 = col3.text_area("入れ込みたい要素③")
  youso3 = col4.text_area("入れ込みたい要素④")
  youso4 = col5.text_area("入れ込みたい要素⑤")

 else:
    # URLを入力する新たな入力欄
    question = st.text_input('URLを入力してください')

 num_elements = st.number_input("出力したいアイデア数を入力してください", min_value=0, value=1, step=1)

# ソーシャルメディアの選択
 social_media = st.selectbox('プラットフォームの選択', ['Twitter', 'Instagram'])

 emoji = st.radio("絵文字とハッシュタグの利用有無",("はい","いいえ"))


 # モデル選択のセレクトボックス
 model = st.selectbox('GPTモデルの選択', ['gpt-3.5-turbo', 'gpt-4'],help="GPT4 での実行はChatGPT Plus への加入が必要です")

 # 実行ボタン
 run_button = st.button('実行')

 if run_button:
    if question != "" and api_key != "":
        emoji_prompt = " 絵文字とハッシュタグを入れて" if emoji == "はい" else ""
        # ChatGPT に質問を送信して回答を生成
        if content_gen == 'リンクから生成':
            response = requests.get(question)
            # BeautifulSoupでHTMLを解析します
            soup = BeautifulSoup(response.text, 'html.parser')
            # 全てのテキストを取得します
            html = ' '.join(map(lambda p: p.text, soup.find_all('p')))
            if social_media == 'Twitter':
             prompt = "商品を説明するPR投稿文を、文章を基にしてTwitter用に"+emoji_prompt+"日本語で140文字以内で"+str(num_elements) +"個考えてください。要素のすべてを入れる必要はありません。文章："+ html
            else: 
             prompt =  "商品を説明するPR文章を、PR文章基礎をベースに入れ込みたい要素を基にしてInstagram用に"+emoji_prompt+"日本語で"+str(num_elements) +"個考えてください。商品：" +promotion + "PR文章基礎:"+question+"入れ込みたい要素："+ html
        else: 
         elements = [youso, youso1, youso2, youso3, youso4]
         elements_md = "\n".join([f"- {el}" for el in elements if el])
         if social_media == 'Twitter':
            prompt = "商品を説明するPR文章を、PR文章基礎をベースに入れ込みたい要素を基にしてTwitter用に"+emoji_prompt+"日本語で140文字以内で"+str(num_elements) +"個考えてください。要素のすべてを入れる必要はありません。商品:" +promotion + "PR文章基礎:"+question+"入れ込みたい要素："+ elements_md
         else: 
            prompt =  "商品を説明するPR文章を、PR文章基礎をベースに入れ込みたい要素を基にしてInstagram用に"+emoji_prompt+"日本語で"+str(num_elements) +"個考えてください。商品：" +promotion + "PR文章基礎:"+question+"入れ込みたい要素："+ elements_md
        headers = {
            "Authorization": f"Bearer {st.session_state.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a Ads Creative Manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            try:
                answer = response.json()["choices"][0]["message"]["content"].strip()
                st.subheader("回答:")
                st.write(answer)


            except KeyError:
                st.error("Failed to retrieve answer from the API response.")
        else:
            try:
                error_details = response.json()
            except ValueError:
                error_details = "No additional information."
            st.error(f"API request failed with status code: {response.status_code}. Details: {error_details}")

with tab3:
    api_key2 = st.secrets["api_key"]["api_key"]
    st.session_state.api_key = api_key

    input_option = st.selectbox('入力形式の選択', ['Text', 'Image'])

    if input_option == 'Text':
        # ユーザーからの質問をテキストボックスで受け取る
        adstext = st.text_area("判定するテキスト")
        prompt = adstext
    else:
        uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.write("読み込みが終了すると実行ボタンが表示されます。")
            # PILのImageオブジェクトをNumPy配列に変換
            image = np.array(image)
            reader = easyocr.Reader(['en', 'ja'])  # 英語と日本語に設定
            result = reader.readtext(image)
            # 結果を表示
            prompt = ' '.join([res[1] for res in result])

    law = st.selectbox('判定する法律を選択', ['薬機法', '景品表示法'])
    model2 = st.selectbox('GPTモデルの選択', ['gpt-3.5-turbo', 'gpt-4'], help="GPT4 での実行はChatGPT Plus への加入が必要です" , key="model_select")

    run_button2 = st.button('実行', key="run_button2")

    if run_button2 and api_key2 != "" and prompt != "":
        if law == '薬機法':
            Rprompt = "以下文章は日本の薬機法に違反するか？また、違反しうる場合、何条に抵触するか考えられるか。法的な助言を提供することはできないことを前提に一般的な情報を日本語で提供してほしい。" + prompt
        else:
            Rprompt = "以下文章は日本の景品表示法に違反するか？また、違反しうる場合、何条に抵触するか考えられるか。法的な助言を提供することはできないことを前提に一般的な情報を日本語で提供してほしい。" + prompt

        headers = {
            "Authorization": f"Bearer {api_key2}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model2,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a legal expert."
                },
                {
                    "role": "user",
                    "content": Rprompt
                }
            ]
        }
        response2 = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

        if response2.status_code == 200:
            try:
                answer2 = response2.json()["choices"][0]["message"]["content"].strip()
                st.subheader("回答:")
                st.write(answer2)
            except KeyError:
                st.error("Failed to retrieve answer from the API response.")
        else:
            try:
                error_details2 = response2.json()
            except ValueError:
                error_details2 = "No additional information."
            st.error(f"API request failed with status code: {response2.status_code}. Details: {error_details2}")

with tab2:
    api_key = st.secrets["api_key"]["api_key"]
    st.session_state.api_key = api_key
   
    st.warning("出力できる画像数は1か月あたり15枚までとなります。")

    promotion = st.text_input("商材名",key="promotion2")
    question = st.text_area("商材の特長",key="question2")

    col1, col2 = st.columns(2)

    youso = col1.text_area("入れ込みたい要素①",key="youso1")
    youso1 = col2.text_area("入れ込みたい要素②",key="youso2")

    col3, col4, col5 = st.columns(3)
    youso2 = col3.text_area("入れ込みたい要素③",key="youso3")
    youso3 = col4.text_area("入れ込みたい要素④",key="youso4")
    youso4 = col5.text_area("入れ込みたい要素⑤",key="youso5")

    num_elements = st.number_input("出力したい画像数を入力してください", min_value=0, value=1, step=1)

    model = st.selectbox('GPTモデルの選択', ['gpt-3.5-turbo', 'gpt-4'], help="GPT4 での実行はChatGPT Plus への加入が必要です" , key="model_select2")

    run_button = st.button('実行' , key="runbotton2")

    if run_button:
        if question != "" and api_key != "":
            elements = [youso, youso1, youso2, youso3, youso4]
            elements_md = "\n".join([f"- {el}" for el in elements if el])
            prompt = "以下の要素をもとに、広告にありそうな構図をDALL-E2に描いてもらいたい。DALL-E2 に入力するプロンプトを英語で考えて。商品:" +promotion + "PR文章基礎:"+question+"入れ込みたい要素："+ elements_md

            headers = {
                "Authorization": f"Bearer {st.session_state.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a Ads Creative Manager."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

            response_data = response.json()

            #チャットGPTの回答を取り出します
            chat_gpt_response = response_data['choices'][0]['message']['content']



            # DALL-Eリクエストの実装
            payload = {
                'n': num_elements,
                'size' : '1024x1024',
                'prompt': chat_gpt_response
            }

            # DALL-E APIのURL
            dall_e_url = 'https://api.openai.com/v1/images/generations'
            headers = {
            'Authorization':'Bearer '+ api_key,
            'Content-type': 'application/json',
            'X-Slack-No-Retry': '1'
            }

            # DALL-Eリクエストの送信
            image_response = requests.post(dall_e_url, headers=headers, json=payload)

            image_response_json = image_response.json()
      
            # 生成された画像のURLを返す
            image_url =  [result['url'] for result in image_response_json['data']]
    

            # Streamlitを用いて画像を表示
            st.image(image_url)
