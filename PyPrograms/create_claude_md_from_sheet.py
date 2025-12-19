"""
CLAUDE.md generator from Google Sheets
Reads business card data from Google Sheets and creates a markdown file
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = r'C:\Users\taman\.gemini\tk-service-account-key.json'
SPREADSHEET_ID = '1lN-ClkkRDO9wdcv8IPWXrRTcHjaQC5kiFC3mHxi2jWA'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def read_spreadsheet():
    """Googleスプレッドシートから名刺情報を読み取る"""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    # スプレッドシートのデータを取得
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A:Z'  # 全カラムを取得
    ).execute()

    values = result.get('values', [])
    return values

def create_claude_md(data):
    """CLAUDE.mdファイルを作成"""
    if not data:
        print("データが見つかりませんでした。")
        return

    with open('CLAUDE.md', 'w', encoding='utf-8') as f:
        f.write("# 名刺データベース\n\n")
        f.write("このファイルは、Google Driveの名刺フォルダ（1eS10Nev-HfnisoY-sPEvephLBQ2h37Lu）内の\n")
        f.write("PDFファイルから読み取った名刺情報をまとめたものです。\n\n")
        f.write("データソース: [名刺リストスプレッドシート](https://docs.google.com/spreadsheets/d/1lN-ClkkRDO9wdcv8IPWXrRTcHjaQC5kiFC3mHxi2jWA)\n\n")

        # ヘッダー行を取得
        if len(data) > 0:
            headers = data[0]
            # マークダウンテーブルのヘッダーを作成
            f.write("| " + " | ".join(headers) + " |\n")
            f.write("|" + "|".join([" --- " for _ in headers]) + "|\n")

            # データ行を追加
            for row in data[1:]:
                # 行の長さをヘッダーに合わせる
                while len(row) < len(headers):
                    row.append("")
                f.write("| " + " | ".join(row[:len(headers)]) + " |\n")

    print(f"CLAUDE.mdを作成しました。{len(data)-1}件の名刺情報を含んでいます。")

def main():
    print("Googleスプレッドシートからデータを読み取り中...")
    data = read_spreadsheet()

    if data:
        print(f"{len(data)}行のデータを取得しました。")
        create_claude_md(data)
    else:
        print("データが見つかりませんでした。")

if __name__ == '__main__':
    main()
