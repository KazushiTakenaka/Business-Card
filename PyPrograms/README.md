# PyPrograms - 名刺管理システム

Google DriveとGoogle Sheetsを使用した名刺管理システムのPythonスクリプト集です。

## スクリプト一覧

### メインスクリプト

- **`main.py`** - メニュー形式のCLIインターフェース
  - すべての機能を統合したメインプログラム
  - 使い方: `python PyPrograms/main.py`

### 個別スクリプト

- **`inspect_drive.py`** - Google Driveフォルダ内の全ファイルをリスト
  - 使い方: `python PyPrograms/inspect_drive.py`
  - すべてのファイルタイプを表示

- **`list_pdfs.py`** - PDFファイルのみをリスト
  - 使い方: `python PyPrograms/list_pdfs.py`
  - PDF形式のファイルのみをフィルタリングして表示

- **`create_claude_md_from_sheet.py`** - GoogleスプレッドシートからCLAUDE.mdを生成
  - 使い方: `python PyPrograms/create_claude_md_from_sheet.py`
  - スプレッドシートのデータをマークダウンテーブルに変換

- **`download_pdf.py`** - PDFファイルをローカルにダウンロード
  - 使い方: `python PyPrograms/download_pdf.py`
  - 確認プロンプト付きで全PDFをダウンロード

- **`extract_and_upload_to_sheet.py`** - PDF名刺情報抽出ワークフロー
  - 使い方:
    - 準備: `python PyPrograms/extract_and_upload_to_sheet.py`
    - クリーンアップ: `python PyPrograms/extract_and_upload_to_sheet.py --cleanup`
  - PDFをダウンロードし、Claude Codeで処理後、クリーンアップする3ステップワークフロー
  - 詳細: `Workflow/pdf_extraction_workflow.md`参照

- **`add_cards_batch.py`** - JSONファイルから名刺データを一括追加
  - 使い方: `python PyPrograms/add_cards_batch.py [JSONファイルパス]`
  - 複数の名刺データを含むJSONファイルを読み込み、スプレッドシートに一括追加
  - JSONテンプレート: `PyPrograms/card_data_template.json`

### ユーティリティモジュール

- **`config.py`** - 設定値の集中管理
  - サービスアカウントファイルのパス
  - Google DriveフォルダID
  - GoogleスプレッドシートID
  - APIスコープの定義

- **`utils.py`** - 共通ユーティリティ関数
  - `get_drive_service()` - Google Drive APIサービス取得
  - `get_sheets_service()` - Google Sheets APIサービス取得
  - `list_files_in_folder()` - フォルダ内ファイルのリスト取得
  - `read_sheet_data()` - スプレッドシートデータの読み取り

## 使用方法

### 環境のセットアップ

```bash
# 仮想環境を有効化
.venv\Scripts\activate  # Windows

# 依存関係をインストール（初回のみ）
pip install -r requirements.txt
```

### メニュー形式で使用

```bash
python PyPrograms/main.py
```

### 個別スクリプトの実行

```bash
# Driveフォルダの内容を確認
python PyPrograms/inspect_drive.py

# PDFファイルのみをリスト
python PyPrograms/list_pdfs.py

# CLAUDE.mdを生成
python PyPrograms/create_claude_md_from_sheet.py

# PDFをダウンロード
python PyPrograms/download_pdf.py
```

## 設定

すべての設定は `config.py` で管理されています：

- **SERVICE_ACCOUNT_FILE**: サービスアカウントキーのパス
- **DRIVE_FOLDER_ID**: 名刺PDFが保存されているGoogle DriveフォルダのID
- **SPREADSHEET_ID**: 名刺データが記録されているGoogleスプレッドシートのID

## 必要な権限

サービスアカウントには以下の権限が必要です：

- Google Drive: フォルダとファイルへの読み取りアクセス
- Google Sheets: スプレッドシートへの読み取りアクセス

## JSONファイルから名刺を一括追加する方法

### 1. JSONファイルを作成

テンプレートをコピーして編集：

```bash
cp PyPrograms/card_data_template.json my_cards.json
```

JSONファイルの例：

```json
{
  "source_pdf": "スキャン_20251217-0754.pdf",
  "cards": [
    [
      "山田 太郎",
      "Taro Yamada",
      "株式会社サンプル",
      "代表取締役",
      "yamada@example.com",
      "090-1234-5678",
      "03-1234-5678",
      "03-1234-5679",
      "100-0001",
      "東京都千代田区千代田1-1-1",
      "https://example.com",
      "",
      "",
      "備考欄"
    ],
    [
      "佐藤 花子",
      "Hanako Sato",
      "サンプル株式会社",
      ...
    ]
  ]
}
```

### 2. スクリプトを実行

```bash
# コマンドラインで指定
python PyPrograms/add_cards_batch.py my_cards.json

# または対話的に入力
python PyPrograms/add_cards_batch.py

# またはメニューから
python PyPrograms/main.py
# メニューで「7」を選択
```

## 出力ファイル

- **CLAUDE.md**: プロジェクトルートに生成される名刺データベースのマークダウンファイル
- **downloaded_pdfs/**: ダウンロードしたPDFファイルの保存ディレクトリ
- **temp_pdfs/**: PDF処理ワークフロー用の一時ディレクトリ
- **processing_data.json**: PDF処理ワークフロー用のメタデータファイル
