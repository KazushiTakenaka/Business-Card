"""
Utility functions for Google API operations
"""

import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from . import config

def get_drive_service(scopes=None):
    """
    Google Drive APIサービスを取得

    Args:
        scopes: APIスコープのリスト。デフォルトはreadonly

    Returns:
        Google Drive APIサービスオブジェクト
    """
    if scopes is None:
        scopes = config.SCOPES_DRIVE_READONLY

    creds = service_account.Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE, scopes=scopes)

    return build('drive', 'v3', credentials=creds)

def get_sheets_service(scopes=None):
    """
    Google Sheets APIサービスを取得

    Args:
        scopes: APIスコープのリスト。デフォルトはreadonly

    Returns:
        Google Sheets APIサービスオブジェクト
    """
    if scopes is None:
        scopes = config.SCOPES_SHEETS_READONLY

    creds = service_account.Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE, scopes=scopes)

    return build('sheets', 'v4', credentials=creds)

def list_files_in_folder(folder_id, mime_type=None, order_by='name'):
    """
    指定されたフォルダ内のファイルをリスト

    Args:
        folder_id: Google DriveフォルダID
        mime_type: フィルタリングするMIMEタイプ（例: 'application/pdf'）
        order_by: ソート順（デフォルト: 'name'）

    Returns:
        ファイルのリスト
    """
    service = get_drive_service(config.SCOPES_DRIVE_METADATA)

    query_parts = [f"'{folder_id}' in parents", "trashed = false"]
    if mime_type:
        query_parts.append(f"mimeType='{mime_type}'")

    query = " and ".join(query_parts)

    results = service.files().list(
        q=query,
        pageSize=100,
        orderBy=order_by,
        fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime)"
    ).execute()

    return results.get('files', [])

def read_sheet_data(spreadsheet_id, range_name='A:Z'):
    """
    Google Sheetsからデータを読み取る

    Args:
        spreadsheet_id: スプレッドシートID
        range_name: 読み取る範囲（デフォルト: 'A:Z'）

    Returns:
        シートデータ（2次元配列）
    """
    service = get_sheets_service()

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    return result.get('values', [])

def append_row_to_sheet(spreadsheet_id, values, range_name='A:A'):
    """
    Google Sheetsに行を追加する

    Args:
        spreadsheet_id: スプレッドシートID
        values: 追加する値のリスト（1行分）
        range_name: 追加する範囲（デフォルト: 'A:A'）

    Returns:
        APIレスポンス
    """
    service = get_sheets_service(config.SCOPES_SHEETS_READWRITE)

    body = {
        'values': [values]
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    return result

def download_file(file_id, file_name=None):
    """
    Google Driveからファイルをダウンロードしてバイトデータを返す

    Args:
        file_id: Google DriveファイルID
        file_name: ファイル名（ログ用、省略可）

    Returns:
        ファイルのバイトデータ
    """
    service = get_drive_service(config.SCOPES_DRIVE_READONLY)

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    fh.seek(0)
    return fh.read()

def move_file_to_folder(file_id, destination_folder_id):
    """
    Google Driveのファイルを別のフォルダに移動する

    Args:
        file_id: 移動するファイルのID
        destination_folder_id: 移動先フォルダのID

    Returns:
        APIレスポンス
    """
    service = get_drive_service(config.SCOPES_DRIVE_READWRITE)

    # 現在の親フォルダを取得
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents', []))

    # ファイルを移動（親フォルダを変更）
    file = service.files().update(
        fileId=file_id,
        addParents=destination_folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()

    return file
