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

## 出力ファイル

- **CLAUDE.md**: プロジェクトルートに生成される名刺データベースのマークダウンファイル
- **downloaded_pdfs/**: ダウンロードしたPDFファイルの保存ディレクトリ
