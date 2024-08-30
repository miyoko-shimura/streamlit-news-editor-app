import streamlit as st
import google.generativeai as genai
from google.api_core import retry
import os
from dotenv import load_dotenv
import PyPDF2
from docx import Document

# Load environment variables
load_dotenv()

# 記事の文体リスト (より一般的なスタイル)
styles = ["ですます調", "である調", "ニュースレポート", "カジュアル", "フォーマル"]

st.title("📰 文章生成アプリ")

# サイドバーでAPIキーを入力
with st.sidebar:
    st.header("Gemini API 設定")
    api_key = st.text_input("Gemini API キーを入力", type="password")
    
    if api_key:
        # Gemini APIの設定
        genai.configure(api_key=api_key)
    else:
        st.warning("APIキーを入力してください。")

# ファイルアップローダーを一番上に配置
uploaded_file = st.file_uploader("ファイルをアップロード", type=["txt", "pdf", "docx"])

# 記事設定をメインに配置
st.header("記事設定")
writing_style = st.selectbox("記事の文体を選択", styles)

word_count = st.number_input("目標文字数", min_value=100, max_value=1000, value=int(os.getenv("DEFAULT_WORD_COUNT", 300)), step=50)

# 言語の選択肢に中国語、韓国語、ポルトガル語、タガログ語を追加
language_options = ["日本語", "English", "中文", "한국어", "Português", "Tagalog"]
default_language = os.getenv("DEFAULT_LANGUAGE", "日本語")
language = st.radio("言語を選択", language_options, index=language_options.index(default_language) if default_language in language_options else 0)

def read_file_content(file):
    if file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    elif file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() for page in pdf_reader.pages)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        st.error("Unsupported file type")
        return None

if uploaded_file is not None and api_key:
    # ファイルの内容を読み込む
    file_contents = read_file_content(uploaded_file)
    if file_contents:
        st.write("ファイルが正常にアップロードされました。")

        if st.button("記事を生成"):
            with st.spinner("記事を生成中..."):
                prompt = f"""
                以下の内容を「{writing_style}」の文体で、約{word_count}文字の記事にまとめてください。
                言語: {language}

                内容:
                {file_contents}
                """

                # Gemini APIを使用して記事を生成
                @retry.Retry()
                def generate_article():
                    model = genai.GenerativeModel('gemini-pro-1.5')
                    response = model.generate_content(prompt)
                    return response.text

                try:
                    generated_article = generate_article()
                    st.subheader("生成された記事")
                    st.write(generated_article)
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

elif not api_key:
    st.warning("サイドバーでGemini APIキーを入力してください。")
else:
    st.info("記事を生成するには、まずファイルをアップロードしてください。")
