"""
画像OCR（文字起こし）ツール
ChatGPT Vision APIを使用して画像から文字を抽出するStreamlitアプリケーション
"""

import streamlit as st
import base64
import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="画像OCR（文字起こし）ツール",
    page_icon="📝",
    layout="centered"
)

# カスタムCSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        font-family: 'Meiryo', sans-serif;
        font-size: 14px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E8F5E9;
        border: 1px solid #4CAF50;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFEBEE;
        border: 1px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)


def encode_image_to_base64(image_data: bytes) -> str:
    """画像データをBase64エンコードする"""
    return base64.b64encode(image_data).decode('utf-8')


def get_language_prompt(language: str) -> str:
    """言語に応じたプロンプトを生成"""
    prompts = {
        "自動判定": "この画像に含まれる文字をすべて正確に抽出してください。",
        "日本語": "この画像に含まれる日本語の文字をすべて正確に抽出してください。日本語を優先して認識してください。",
        "英語": "Please extract all English text from this image accurately. Prioritize English text recognition."
    }
    return prompts.get(language, prompts["自動判定"])


def perform_ocr(image_data: bytes, file_type: str, language: str) -> str:
    """ChatGPT Vision APIを使用してOCRを実行"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        raise ValueError("APIキーが設定されていません。.envファイルにOPENAI_API_KEYを設定してください。")
    
    client = OpenAI(api_key=api_key)
    
    # 画像をBase64エンコード
    base64_image = encode_image_to_base64(image_data)
    
    # MIMEタイプの決定
    mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp"
    }
    mime_type = mime_types.get(file_type.lower(), "image/png")
    
    # プロンプトの作成
    user_prompt = get_language_prompt(language)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "あなたはOCR専門AIです。画像内の文字を正確に抽出してください。文字のみを返し、不要な説明文は含めないでください。改行やレイアウトは可能な限り維持してください。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
            timeout=60
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_message = str(e)
        if "timeout" in error_message.lower():
            raise TimeoutError("処理がタイムアウトしました。もう一度お試しください。")
        else:
            raise RuntimeError(f"OCR処理に失敗しました: {error_message}")


def main():
    # タイトル
    st.markdown("<h1 class='main-title'>📝 画像OCR（文字起こし）ツール</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # サイドバー情報
    with st.sidebar:
        st.header("ℹ️ 使い方")
        st.markdown("""
        1. 画像をアップロード
        2. 言語を選択（任意）
        3. 「文字起こしを実行」をクリック
        4. 結果をコピー
        """)
        st.markdown("---")
        st.markdown("**対応形式**: PNG, JPG, JPEG, WEBP")
        st.markdown("**最大サイズ**: 5MB")
    
    # ファイルアップロード
    uploaded_file = st.file_uploader(
        "画像ファイルを選択してください",
        type=["png", "jpg", "jpeg", "webp"],
        help="PNG, JPG, JPEG, WEBP形式に対応（最大5MB）"
    )
    
    # 言語選択
    language = st.selectbox(
        "言語選択（任意）",
        options=["自動判定", "日本語", "英語"],
        help="抽出する文字の言語を指定できます"
    )
    
    # 画像がアップロードされた場合
    if uploaded_file is not None:
        # ファイルサイズチェック（5MB制限）
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        
        if file_size_mb > 5:
            st.error(f"⚠️ ファイルサイズが大きすぎます（{file_size_mb:.1f}MB）。5MB以下のファイルを選択してください。")
        else:
            # 画像プレビュー
            st.subheader("📷 アップロード画像")
            st.image(uploaded_file, use_container_width=True)
            
            # ファイル情報表示
            file_ext = uploaded_file.name.split('.')[-1].lower()
            st.caption(f"ファイル名: {uploaded_file.name} | サイズ: {file_size_mb:.2f}MB")
            
            st.markdown("---")
            
            # 実行ボタン
            if st.button("🔍 文字起こしを実行", type="primary", use_container_width=True):
                with st.spinner("OCR処理中..."):
                    try:
                        # 画像データの取得
                        image_data = uploaded_file.getvalue()
                        
                        # OCR実行
                        result = perform_ocr(image_data, file_ext, language)
                        
                        # セッション状態に結果を保存
                        st.session_state['ocr_result'] = result
                        st.session_state['ocr_success'] = True
                        
                    except ValueError as e:
                        st.error(f"⚠️ {str(e)}")
                        st.session_state['ocr_success'] = False
                    except TimeoutError as e:
                        st.error(f"⏱️ {str(e)}")
                        st.session_state['ocr_success'] = False
                    except RuntimeError as e:
                        st.error(f"❌ {str(e)}")
                        st.session_state['ocr_success'] = False
                    except Exception as e:
                        st.error(f"❌ 予期しないエラーが発生しました: {str(e)}")
                        st.session_state['ocr_success'] = False
            
            # 結果表示
            if st.session_state.get('ocr_success') and 'ocr_result' in st.session_state:
                st.subheader("📄 抽出結果")
                
                # 編集可能なテキストエリア
                result_text = st.text_area(
                    "抽出されたテキスト（編集可能）",
                    value=st.session_state['ocr_result'],
                    height=300,
                    key="result_area"
                )
                
                # コピー用コードブロック
                st.code(result_text, language=None)
                
                st.success("✅ 文字起こしが完了しました。上のコードブロックからテキストをコピーできます。")


if __name__ == "__main__":
    main()
