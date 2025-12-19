"""
Google Drive folder inspector
Lists all files in the business card folder on Google Drive
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'
PARENT_FOLDER_ID = '1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    print(f"Listing files in folder ID: {PARENT_FOLDER_ID}")

    query = f"'{PARENT_FOLDER_ID}' in parents and trashed = false"

    results = service.files().list(
        q=query,
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']}) - {item['mimeType']}")

if __name__ == '__main__':
    main()
