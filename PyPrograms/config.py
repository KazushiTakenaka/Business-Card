"""
Configuration file for business card management system
Centralizes all configuration constants
"""

# Service Account Configuration
SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'

# Google Drive Configuration
DRIVE_FOLDER_ID = '1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu'
PROCESSED_FOLDER_ID = '1Ddb0n_BYW35KMU-nzKzZfrv8c5oBccNe'  # 読み取り済データフォルダ

# Google Sheets Configuration
SPREADSHEET_ID = '1lN-ClkkRDO9wdcv8IPWXrRTcHjaQC5kiFC3mHxi2jWA'

# API Scopes
SCOPES_DRIVE_READONLY = ['https://www.googleapis.com/auth/drive.readonly']
SCOPES_DRIVE_METADATA = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES_DRIVE_READWRITE = ['https://www.googleapis.com/auth/drive']
SCOPES_SHEETS_READONLY = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES_SHEETS_READWRITE = ['https://www.googleapis.com/auth/spreadsheets']

# Output Configuration
OUTPUT_MARKDOWN_FILE = 'CLAUDE.md'
DOWNLOAD_DIR = 'downloaded_pdfs'
