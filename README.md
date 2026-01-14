# 画像OCR（文字起こし）ツール

ChatGPT Vision APIを使用して画像から文字を抽出するWebアプリケーションです。

## 機能

- 画像アップロード（PNG, JPG, JPEG, WEBP対応）
- ChatGPT Vision APIによる高精度OCR
- 言語選択（自動判定/日本語/英語）
- 抽出結果の編集・コピー

## セットアップ

### 1. 仮想環境の作成

```bash
cd "c:\Users\hikko\OneDrive\ドキュメント\Antigravity ファイル\Image text"
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. パッケージのインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーの設定

`.env.example` を `.env` にコピーして、OpenAI APIキーを設定してください。

```bash
copy .env.example .env
```

`.env` ファイルを編集:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

## 起動方法

```bash
.\.venv\Scripts\activate
streamlit run app.py
```

ブラウザが自動的に開き、アプリケーションが表示されます。

## 使用方法

1. 「画像ファイルを選択してください」から画像をアップロード
2. 必要に応じて言語を選択（自動判定/日本語/英語）
3. 「文字起こしを実行」ボタンをクリック
4. 抽出されたテキストをコピー

## 対応ファイル形式

- PNG
- JPG / JPEG
- WEBP
- 最大ファイルサイズ: 5MB

## 注意事項

- OpenAI APIの利用料金が発生します
- 画像はサーバーに保存されません（メモリ処理のみ）
