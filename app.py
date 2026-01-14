"""
画像OCR（文字起こし）ツール
ChatGPT Vision APIを使用して画像から文字を抽出するStreamlitアプリケーション
カフェ風デザイン
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
    page_icon="☕",
    layout="centered"
)

# カフェ風カスタムCSS（ベージュ背景）
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Playfair+Display:wght@400;600;700&display=swap');
    
    /* 全体の背景 - 温かみのあるベージュ */
    .stApp {
        background: linear-gradient(135deg, #F5F0E8 0%, #EDE4D8 50%, #F8F4EE 100%);
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    /* メインコンテナ */
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 2rem 3rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(139, 109, 76, 0.15);
        border: 1px solid rgba(139, 109, 76, 0.1);
    }
    
    /* タイトルスタイル */
    .cafe-title {
        text-align: center;
        color: #5D4E37;
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .cafe-subtitle {
        text-align: center;
        color: #8B6D4C;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    /* ロゴアイコン */
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        font-size: 4rem;
        display: inline-block;
    }
    
    /* 区切り線 */
    .cafe-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #C4A77D, transparent);
        margin: 1.5rem 0;
        border: none;
    }
    
    /* ファイルアップローダー */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, #FDFCFA, #F9F6F1);
        border: 2px dashed #C4A77D;
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #8B6D4C;
        background: linear-gradient(135deg, #FFF9F0, #FDF8F3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 109, 76, 0.15);
    }
    
    /* セレクトボックス */
    .stSelectbox > div > div {
        background: #FDFCFA;
        border: 2px solid #D4C4B0;
        border-radius: 10px;
        color: #5D4E37;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #8B6D4C;
        box-shadow: 0 3px 10px rgba(139, 109, 76, 0.15);
    }
    
    /* ボタン */
    .stButton > button {
        background: linear-gradient(135deg, #8B6D4C, #6B5344);
        color: #FFF9F0;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 109, 76, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #6B5344, #8B6D4C);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(139, 109, 76, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* テキストエリア */
    .stTextArea textarea {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: 14px;
        border: 2px solid #E5DCD1;
        border-radius: 15px;
        background: #FDFCFA;
        color: #3D3425;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #8B6D4C;
        box-shadow: 0 0 10px rgba(139, 109, 76, 0.15);
    }
    
    /* ラベルテキスト */
    .stTextArea label, .stSelectbox label, .stFileUploader label {
        color: #5D4E37 !important;
        font-weight: 500;
    }
    
    /* サクセスメッセージ */
    .stSuccess {
        background: linear-gradient(135deg, #F0EBE3, #E8E0D5);
        border-left: 4px solid #8B6D4C;
        border-radius: 10px;
        color: #5D4E37;
    }
    
    /* エラーメッセージ */
    .stError {
        background: linear-gradient(135deg, #F8E8E8, #F5D5D5);
        border-left: 4px solid #B85450;
        border-radius: 10px;
    }
    
    /* サイドバー */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E8DFD3 0%, #D4C4B0 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #5D4E37;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #4A3C2A;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #5D4E37;
    }
    
    /* マークダウンテキスト */
    .stMarkdown h3 {
        color: #5D4E37;
        font-weight: 600;
        border-bottom: 2px solid #C4A77D;
        padding-bottom: 0.5rem;
    }
    
    /* 画像プレビュー */
    .stImage {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(139, 109, 76, 0.15);
        border: 3px solid #E8DFD3;
    }
    
    /* キャプション */
    .stCaption {
        color: #8B6D4C;
        font-style: italic;
    }
    
    /* コードブロック */
    .stCode {
        border-radius: 10px;
        border: 1px solid #E5DCD1;
        background: #FDFCFA;
    }
    
    /* スピナー */
    .stSpinner > div {
        border-color: #8B6D4C;
    }
    
    /* フッター */
    .footer {
        text-align: center;
        color: #8B6D4C;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #D4C4B0;
        font-style: italic;
    }
    
    /* デコレーション */
    .coffee-beans {
        text-align: center;
        font-size: 1.5rem;
        letter-spacing: 10px;
        margin: 0.5rem 0;
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
    # ロゴとタイトル
    st.markdown("""
        <div class="logo-container">
            <span class="logo-icon">☕</span>
        </div>
        <h1 class="cafe-title">IMAGE OCR TOOL</h1>
        <p class="cafe-subtitle">〜 画像から文字を抽出 〜</p>
        <div class="coffee-beans">☕ ✦ ☕ ✦ ☕</div>
        <div class="cafe-divider"></div>
    """, unsafe_allow_html=True)
    
    # サイドバー情報
    with st.sidebar:
        st.markdown("## ☕ 使い方")
        st.markdown("""
        1. 📷 画像をアップロード
        2. 🌐 言語を選択（任意）
        3. ▶️ 「文字起こしを実行」をクリック
        4. 📋 結果をコピー
        """)
        st.markdown("---")
        st.markdown("**📁 対応形式**")
        st.markdown("PNG, JPG, JPEG, WEBP")
        st.markdown("**📦 最大サイズ**")
        st.markdown("5MB")
        st.markdown("---")
        st.markdown("*Powered by ChatGPT Vision API*")
    
    # ファイルアップロード
    uploaded_file = st.file_uploader(
        "☕ 画像ファイルをドロップまたは選択",
        type=["png", "jpg", "jpeg", "webp"],
        help="PNG, JPG, JPEG, WEBP形式に対応（最大5MB）"
    )
    
    # 言語選択
    language = st.selectbox(
        "🌐 言語選択（任意）",
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
            st.markdown("### 📷 アップロード画像")
            st.image(uploaded_file, use_container_width=True)
            
            # ファイル情報表示
            file_ext = uploaded_file.name.split('.')[-1].lower()
            st.caption(f"📄 {uploaded_file.name} | 📦 {file_size_mb:.2f}MB")
            
            st.markdown('<div class="cafe-divider"></div>', unsafe_allow_html=True)
            
            # 実行ボタン
            if st.button("☕ 文字起こしを実行", type="primary", use_container_width=True):
                with st.spinner("✨ OCR処理中...しばらくお待ちください"):
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
                st.markdown("### 📄 抽出結果")
                
                # 編集可能なテキストエリア
                result_text = st.text_area(
                    "抽出されたテキスト（編集可能）",
                    value=st.session_state['ocr_result'],
                    height=300,
                    key="result_area"
                )
                
                # コピー用コードブロック
                st.code(result_text, language=None)
                
                st.success("✅ 文字起こしが完了しました！上のコードブロックからテキストをコピーできます。")
    
    # フッター
    st.markdown("""
        <div class="footer">
            ✦ Made with ☕ & 🤎 | Image OCR Tool ✦
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
