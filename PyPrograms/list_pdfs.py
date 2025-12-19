"""
List PDF files in Google Drive folder
Filters and displays only PDF files from the business card folder
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'
PARENT_FOLDER_ID = '1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    """PDFファイルのみをリストアップ"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    # PDFファイルのみを検索
    query = f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/pdf' and trashed = false"

    results = service.files().list(
        q=query,
        pageSize=100,
        orderBy='name',
        fields="nextPageToken, files(id, name, createdTime, modifiedTime)").execute()

    items = results.get('files', [])

    if not items:
        print('PDFファイルが見つかりませんでした。')
    else:
        print(f'{len(items)}個のPDFファイルが見つかりました。\n')
        for idx, item in enumerate(items, 1):
            print(f"{idx:3d}. {item['name']}")
            print(f"     ID: {item['id']}")
            print(f"     作成: {item.get('createdTime', 'N/A')}")
            print(f"     更新: {item.get('modifiedTime', 'N/A')}")
            print()

if __name__ == '__main__':
    main()
