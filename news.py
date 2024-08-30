import streamlit as st
import google.generativeai as genai
from google.api_core import retry
import os

# Gemini APIの設定
os.environ[GOOGLE_APPLICATION_CREDENTIALS] = pathtoyourcredentials.json
genai.configure(api_key=os.getenv(GOOGLE_API_KEY))

# 新聞社のリスト
newspapers = [朝日新聞, 読売新聞, 毎日新聞, 日本経済新聞, 産経新聞, その他（自由入力）]

st.title(📰 新聞風記事生成アプリ)

# サイドバーの設定
with st.sidebar
    st.header(設定)
    newspaper_style = st.selectbox(新聞社の文体を選択, newspapers)
    if newspaper_style == その他（自由入力）
        newspaper_style = st.text_input(新聞社名を入力)
    
    word_count = st.number_input(目標文字数, min_value=100, max_value=1000, value=300, step=50)
    language = st.radio(言語を選択, [日本語, English])

# ファイルアップローダー
uploaded_file = st.file_uploader(ファイルをアップロード, type=[txt, pdf, docx])

if uploaded_file is not None
    # ファイルの内容を読み込む
    file_contents = uploaded_file.read().decode(utf-8)
    st.write(ファイルが正常にアップロードされました。)

    if st.button(記事を生成)
        with st.spinner(記事を生成中...)
            prompt = f
            以下の内容を{newspaper_style}の文体で、約{word_count}文字の記事にまとめてください。
            言語 {'日本語' if language == '日本語' else '英語'}

            内容
            {file_contents}
            

            # Gemini APIを使用して記事を生成
            @retry.Retry()
            def generate_article()
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                return response.text

            try
                generated_article = generate_article()
                st.subheader(生成された記事)
                st.write(generated_article)
            except Exception as e
                st.error(fエラーが発生しました {str(e)})

else
    st.info(記事を生成するには、まずファイルをアップロードしてください。)