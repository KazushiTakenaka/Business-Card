"""
Google Drive folder inspector
Lists all files in the business card folder on Google Drive
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

import config

def main():
    creds = service_account.Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE, scopes=config.SCOPES_DRIVE_METADATA)

    service = build('drive', 'v3', credentials=creds)

    print(f"Listing files in folder ID: {config.DRIVE_FOLDER_ID}")

    query = f"'{config.DRIVE_FOLDER_ID}' in parents and trashed = false"

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
