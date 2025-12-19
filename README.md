# 名刺管理システム

Google DriveとGoogle Sheetsを連携した名刺管理システムです。スキャンした名刺PDFをGoogle Driveに保存し、名刺情報をGoogle Sheetsで一元管理します。

## 主な機能

- **Google Drive連携**: 名刺PDFファイルの一覧表示・ダウンロード
- **Google Sheets連携**: 名刺情報データベースの管理
- **PDF情報抽出ワークフロー**: PDFから名刺情報を抽出してスプレッドシートに登録
- **インタラクティブメニュー**: コマンドラインから簡単に各機能を実行

## セットアップ

### 1. 前提条件

- Python 3.8以上
- Google Cloud サービスアカウント（認証情報）
- Google Drive、Google Sheetsへのアクセス権限

### 2. 仮想環境のセットアップ

```bash
# 仮想環境の有効化（Windows）
.venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 3. 認証設定

サービスアカウントキーファイルを配置:
```
C:\Users\taman\.gemini\tk-service-account-key.json
```

### 4. Google リソースID

- **Google Drive フォルダID**: `1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu`
- **Google Sheets ID**: `1lN-ClkkRDO9wdcv8IPWXrRTcHjaQC5kiFC3mHxi2jWA`

## 使い方

### インタラクティブメニューの起動

```bash
# 仮想環境を有効化
.venv\Scripts\activate

# メニューを起動
python PyPrograms/main.py
```

メニューから以下の操作が可能です:

1. Google Driveファイル一覧の表示
2. PDFファイル一覧の表示
3. PDFファイルのダウンロード
4. CLAUDE.mdの生成（スプレッドシートから）
5. PDF準備（temp_pdfsフォルダへダウンロード）
6. 一時ファイルのクリーンアップ
7. JSONデータのスプレッドシートへの追加

### PDF名刺情報抽出ワークフロー

詳細は [Workflow/pdf_extraction_workflow.md](Workflow/pdf_extraction_workflow.md) を参照してください。

**クイックスタート:**

```bash
# ステップ1: PDF準備（メニューで「5」を選択）
# ステップ2: Claude Codeで名刺情報抽出
# ステップ3: JSONをスプレッドシートに追加（メニューで「7」を選択）
# ステップ4: クリーンアップ（メニューで「6」を選択）
```

### 個別スクリプトの実行

```bash
# Drive内の全ファイル一覧
python PyPrograms/inspect_drive.py

# PDFファイル一覧
python PyPrograms/list_pdfs.py

# PDFダウンロード
python PyPrograms/download_pdf.py

# CLAUDE.md生成
python PyPrograms/create_claude_md_from_sheet.py
```

## プロジェクト構造

```
名刺/
├── .venv/                              # Python仮想環境
├── PyPrograms/                         # Pythonスクリプト
│   ├── main.py                        # インタラクティブメニュー
│   ├── config.py                      # 設定ファイル
│   ├── utils.py                       # 共通ユーティリティ
│   ├── inspect_drive.py               # Driveファイル一覧
│   ├── list_pdfs.py                   # PDF一覧
│   ├── download_pdf.py                # PDFダウンロード
│   ├── create_claude_md_from_sheet.py # CLAUDE.md生成
│   ├── extract_and_upload_to_sheet.py # JSON→Sheets追加
│   └── README.md                      # PyPrograms詳細ドキュメント
├── Workflow/                           # ワークフロードキュメント
│   ├── README.md                      # ワークフロー概要
│   └── pdf_extraction_workflow.md     # PDF抽出ワークフロー
├── requirements.txt                    # Python依存パッケージ
├── CLAUDE.md                          # 開発者向け詳細ドキュメント
└── README.md                          # このファイル
```

## 技術スタック

- **Python 3.x**
- **Google Drive API** - PDFファイルの管理
- **Google Sheets API** - 名刺データベースの管理
- **google-api-python-client** - Google APIクライアント
- **google-auth** - 認証ライブラリ

## ドキュメント

- **[CLAUDE.md](CLAUDE.md)**: Claude Code向けの開発ガイド
- **[PyPrograms/README.md](PyPrograms/README.md)**: Pythonスクリプトの詳細
- **[Workflow/pdf_extraction_workflow.md](Workflow/pdf_extraction_workflow.md)**: PDF抽出ワークフロー

## 設計思想

このプロジェクトは**モジュラー設計**に基づいています:

- **単一責任の原則**: 各スクリプトは1つの明確な目的を持つ
- **独立したモジュール**: スクリプトは独立して実行可能
- **シンプル重視**: 過度な抽象化を避け、理解しやすさを優先

詳細は [CLAUDE.md](CLAUDE.md) の「Design Philosophy」セクションを参照してください。

## ライセンス

このプロジェクトは個人利用を目的としています。

## 注意事項

- **読み取り専用アクセス**: 各スクリプトはGoogle APIに対して読み取り専用スコープを使用
- **サービスアカウント認証**: 個人アカウントではなくサービスアカウントで認証
- **UTF-8エンコーディング**: 日本語テキスト処理のため、ファイル出力時はUTF-8を使用
