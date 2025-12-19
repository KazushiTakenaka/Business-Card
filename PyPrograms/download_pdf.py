"""
Download PDF files from Google Drive
Downloads business card PDFs to a local directory
"""

import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'
PARENT_FOLDER_ID = '1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_pdf_files(service):
    """PDFファイルのリストを取得"""
    query = f"'{PARENT_FOLDER_ID}' in parents and mimeType='application/pdf' and trashed = false"

    results = service.files().list(
        q=query,
        pageSize=100,
        orderBy='name',
        fields="nextPageToken, files(id, name)").execute()

    return results.get('files', [])

def download_pdf(service, file_id, file_name, output_dir='downloaded_pdfs'):
    """PDFファイルをダウンロード"""
    # 出力ディレクトリを作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(output_dir, file_name)

    fh = io.FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"  ダウンロード進行: {int(status.progress() * 100)}%")

    print(f"  保存完了: {file_path}")
    return file_path

def main():
    """メイン処理"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=creds)

    print("PDFファイルのリストを取得中...")
    pdf_files = get_pdf_files(service)

    if not pdf_files:
        print("PDFファイルが見つかりませんでした。")
        return

    print(f"{len(pdf_files)}個のPDFファイルが見つかりました。\n")

    # ユーザーに確認
    print("すべてのPDFをダウンロードしますか？ (y/n): ", end='')
    response = input().strip().lower()

    if response != 'y':
        print("キャンセルしました。")
        return

    # ダウンロード
    for idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{len(pdf_files)}] {pdf_file['name']}")
        try:
            download_pdf(service, pdf_file['id'], pdf_file['name'])
        except Exception as e:
            print(f"  エラー: {str(e)}")

    print(f"\n完了！{len(pdf_files)}個のファイルをダウンロードしました。")

if __name__ == '__main__':
    main()
