# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a business card management system that integrates with Google Drive and Google Sheets. It processes scanned business card PDFs stored in a Google Drive folder and maintains structured data in a Google Sheets spreadsheet.

**Key Resources:**
- Google Drive folder ID: `1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu` (contains scanned business card PDFs)
- Google Sheets ID: `1lN-ClkkRDO9wdcv8IPWXrRTcHjaQC5kiFC3mHxi2jWA` (名刺リスト - business card database)
- Service account key: `C:\Users\taman\.gemini\tk-service-account-key.json`

## Environment Setup

### Python Environment

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows

# Install dependencies (if needed)
pip install google-api-python-client google-auth google-auth-httplib2 anthropic
```

### Installed Dependencies

- `google-api-python-client` - Google Drive and Sheets API access
- `google-auth` - Authentication for Google services
- `anthropic` - Claude API client (installed but not currently used)

## Common Commands

### Running Scripts

```bash
# Activate environment first
.venv\Scripts\activate

# Run interactive menu (recommended)
python PyPrograms/main.py

# Or run individual scripts:

# List all files in Google Drive folder
python PyPrograms/inspect_drive.py

# List PDF files with details
python PyPrograms/list_pdfs.py

# Create CLAUDE.md from Google Sheets data
python PyPrograms/create_claude_md_from_sheet.py

# Download all PDFs from Drive
python PyPrograms/download_pdf.py
```

### Working with Google APIs

The project uses a service account for authentication. All scripts should:

1. Load credentials from `C:\Users\taman\.gemini\tk-service-account-key.json`
2. Use appropriate scopes:
   - `https://www.googleapis.com/auth/drive.readonly` for Drive access
   - `https://www.googleapis.com/auth/drive.metadata.readonly` for metadata only
   - `https://www.googleapis.com/auth/spreadsheets.readonly` for Sheets access

## Design Philosophy

This project follows a **modular, function-based design** with the following principles:

### Core Principles

1. **Single Responsibility Principle (SRP)**
   - Each script has one clear, focused purpose
   - `inspect_drive.py` only lists files
   - `list_pdfs.py` only lists PDFs
   - `create_claude_md_from_sheet.py` only generates markdown
   - `download_pdf.py` only downloads files

2. **Modular Architecture**
   - Independent scripts that can be run standalone
   - Shared utilities extracted to `utils.py`
   - Configuration centralized in `config.py`
   - No tight coupling between scripts

3. **Separation of Concerns**
   ```
   PyPrograms/
   ├── main.py                          # UI layer (menu interface)
   ├── inspect_drive.py                 # Individual functions
   ├── list_pdfs.py                     # Individual functions
   ├── create_claude_md_from_sheet.py  # Individual functions
   ├── download_pdf.py                  # Individual functions
   ├── config.py                        # Configuration layer
   └── utils.py                         # Utility layer (API helpers)
   ```

4. **Simple Over Complex**
   - **NOT using Hexagonal Architecture** (too complex for this use case)
   - Direct Google API calls with thin utility wrapper
   - Minimal abstraction layers
   - Easy to understand and maintain

### Why This Design?

This design is appropriate because:

- **Small-scale project**: Limited business logic
- **Simple operations**: API call → data transformation → output
- **Single external dependency**: Google APIs only
- **Utility scripts**: Designed for direct execution, not as a framework
- **Quick development**: No need for complex dependency injection

### When to Use Different Architectures

Consider **Hexagonal Architecture** only if:
- Complex business logic emerges
- Multiple external systems need to be swapped (e.g., Drive → S3)
- High test coverage is critical
- Long-term maintenance by a team is planned

For this project, **keep it simple** with modular scripts and shared utilities.

### Adding New Features

When adding new functionality:

1. **Create a new standalone script** for the main feature
2. **Extract common logic to `utils.py`** if used by multiple scripts
3. **Add configuration to `config.py`** if needed
4. **Update `main.py` menu** to include the new option
5. **Keep scripts independent** - avoid cross-script dependencies

Example: Adding a feature to upload files to Drive
```python
# PyPrograms/upload_to_drive.py
from google.oauth2 import service_account
from googleapiclient.discovery import build
from . import config

def main():
    # Standalone implementation
    # Uses config.py for settings
    # Can be run independently
    pass
```

## Project Architecture

### Data Flow

1. **Source**: Scanned business card PDFs in Google Drive folder
2. **Processing**: Information extracted and stored in Google Sheets
3. **Output**: CLAUDE.md file generated from spreadsheet data

### Google Sheets Structure

The spreadsheet contains the following columns:
- 氏名(漢字) - Name in kanji
- 氏名(ローマ字) - Name in romaji
- 会社名 - Company name
- 役職 - Position/title
- メールアドレス - Email address
- 携帯電話 - Mobile phone
- 固定電話 - Landline phone
- FAX
- 郵便番号 - Postal code
- 住所 - Address
- ウェブサイト - Website
- LINE ID
- その他SNS - Other social media
- 備考 - Notes
- スキャンファイル名 - Scan filename
- 読み取り日 - Date scanned

### Code Patterns

**Google API Authentication:**
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)
```

**Querying Google Drive:**
```python
query = f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/pdf' and trashed = false"
results = service.files().list(q=query, pageSize=100, fields="files(id, name)").execute()
```

**Reading Google Sheets:**
```python
service = build('sheets', 'v4', credentials=creds)
result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='A:Z'
).execute()
values = result.get('values', [])
```

## Important Notes

- **No Claude API usage**: While the Anthropic SDK is installed, this project does NOT use Claude API for PDF processing. The business card data is manually maintained in the Google Sheets.
- **Read-only access**: Scripts use read-only scopes for Google services
- **Character encoding**: Use UTF-8 encoding when writing files (`encoding='utf-8'`)
- **PDF files**: Currently 33 business card PDFs in the Drive folder (as of last check)

## File Organization

```
名刺/
├── .venv/                                # Python virtual environment
├── PyPrograms/                           # Python scripts package
│   ├── __init__.py                       # Package initialization
│   ├── main.py                          # Interactive CLI menu
│   ├── config.py                        # Configuration constants
│   ├── utils.py                         # Common utility functions
│   ├── inspect_drive.py                 # List all Drive files
│   ├── list_pdfs.py                     # List PDF files only
│   ├── create_claude_md_from_sheet.py  # Generate CLAUDE.md from Sheets
│   ├── download_pdf.py                  # Download PDFs from Drive
│   ├── extract_and_upload_to_sheet.py  # PDF extraction workflow script
│   └── README.md                        # PyPrograms documentation
├── Workflow/                             # Workflow documentation
│   ├── README.md                        # Workflow directory overview
│   └── pdf_extraction_workflow.md       # PDF extraction workflow guide
├── requirements.txt                      # Python dependencies
└── CLAUDE.md                            # This file (project documentation)
```

## Typical Workflows

### PDF名刺情報抽出ワークフロー

PDFから名刺情報を抽出してスプレッドシートに登録する完全なワークフロー。

**詳細ドキュメント:** [Workflow/pdf_extraction_workflow.md](Workflow/pdf_extraction_workflow.md)

**クイックスタート:**
```bash
.venv\Scripts\activate
python PyPrograms/main.py
# ステップ1: メニューで「5」を選択してPDF準備
# ステップ2: Claude Codeに「temp_pdfs/内の全PDFから名刺情報を抽出して、extracted_business_cards.jsonに保存してください」と依頼
# ステップ3: メニューで「7」を選択してJSONをスプレッドシートに追加
# ステップ4: メニューで「6」を選択してクリーンアップ
```

**重要な仕様:**
- JSONファイル名は常に`extracted_business_cards.json`（固定）
- JSON形式は配列形式（`[{...}, {...}]`）を推奨
- ファイル名から読み取り日を自動抽出（例: `スキャン_20250803-0909-2.pdf` → `2025-08-03`）
- クリーンアップ時に`extracted_business_cards.json`も自動削除

### Regenerating CLAUDE.md from Spreadsheet

When the Google Sheets data is updated and you need to refresh the CLAUDE.md:

```bash
.venv\Scripts\activate
python PyPrograms/create_claude_md_from_sheet.py
```

This reads the spreadsheet and creates a markdown table with all business card information.

### Checking Drive Folder Contents

To see what PDF files are in the Google Drive folder:

```bash
.venv\Scripts\activate
python PyPrograms/inspect_drive.py
```
