"""
PDF名刺情報抽出とスプレッドシートアップロード
段階的な処理:
1. 準備: PDFをダウンロードしてメタデータを保存
2. 処理: Claude CodeがPDFを読み取ってスプレッドシートに追加（手動）
3. クリーンアップ: ローカルファイルを削除し、DriveファイルをProcessedフォルダに移動
"""

import os
import json
import argparse
import sys

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import list_files_in_folder, download_file, move_file_to_folder

PROCESSING_DATA_FILE = 'processing_data.json'
TEMP_PDF_DIR = 'temp_pdfs'
EXTRACTED_JSON_FILE = 'extracted_business_cards.json'

def prepare_pdfs():
    """
    ステップ1: PDFをダウンロードして処理準備
    """
    print("=" * 60)
    print("ステップ1: PDFダウンロードと準備")
    print("=" * 60)

    # PDFファイルのリストを取得
    print("\nGoogle DriveからPDFファイルリストを取得中...")
    pdf_files = list_files_in_folder(
        config.DRIVE_FOLDER_ID,
        mime_type='application/pdf'
    )

    if not pdf_files:
        print("処理対象のPDFファイルが見つかりませんでした。")
        return

    print(f"{len(pdf_files)}個のPDFファイルが見つかりました。\n")

    # 一時ディレクトリを作成
    if not os.path.exists(TEMP_PDF_DIR):
        os.makedirs(TEMP_PDF_DIR)

    # メタデータを保存するリスト
    processing_data = []

    # 各PDFをダウンロード
    for idx, pdf_file in enumerate(pdf_files, 1):
        file_name = pdf_file['name']
        file_id = pdf_file['id']

        print(f"[{idx}/{len(pdf_files)}] ダウンロード中: {file_name}")

        try:
            # PDFをダウンロード
            pdf_data = download_file(file_id, file_name)

            # 一時ファイルとして保存
            local_path = os.path.join(TEMP_PDF_DIR, file_name)
            with open(local_path, 'wb') as f:
                f.write(pdf_data)

            # メタデータを記録
            processing_data.append({
                'file_name': file_name,
                'file_id': file_id,
                'local_path': local_path,
                'processed': False
            })

            print(f"  保存完了: {local_path}")

        except Exception as e:
            print(f"  エラー: {str(e)}")
            continue

    # メタデータをJSONファイルに保存
    with open(PROCESSING_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(processing_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"準備完了！{len(processing_data)}個のPDFをダウンロードしました。")
    print(f"{'=' * 60}")
    print("\n次のステップ:")
    print("1. Claude Codeに以下のように依頼してください:")
    print(f"   「{TEMP_PDF_DIR}/内の全PDFから名刺情報を抽出して、")
    print(f"    {EXTRACTED_JSON_FILE}に保存してください」")
    print("\n2. JSONファイルをスプレッドシートに追加:")
    print("   python PyPrograms/main.py")
    print("   # メニューで「7」を選択")
    print(f"   または: python PyPrograms/add_cards_batch.py {EXTRACTED_JSON_FILE}")
    print("\n3. 処理完了後、以下のコマンドでクリーンアップを実行:")
    print(f"   python PyPrograms/extract_and_upload_to_sheet.py --cleanup")
    print(f"   または: python PyPrograms/main.py でメニュー「6」を選択")
    print(f"{'=' * 60}\n")

def cleanup_processed_files():
    """
    ステップ3: 処理済みファイルのクリーンアップ
    ローカルファイルを削除し、DriveファイルをProcessedフォルダに移動
    """
    print("=" * 60)
    print("ステップ3: クリーンアップ処理")
    print("=" * 60)

    # メタデータファイルを読み込み
    if not os.path.exists(PROCESSING_DATA_FILE):
        print(f"エラー: {PROCESSING_DATA_FILE}が見つかりません。")
        print("先にPDFの準備（ダウンロード）を実行してください。")
        return

    with open(PROCESSING_DATA_FILE, 'r', encoding='utf-8') as f:
        processing_data = json.load(f)

    if not processing_data:
        print("処理対象のファイルがありません。")
        return

    print(f"\n{len(processing_data)}個のファイルをクリーンアップします。")
    print("\n続行しますか？ (y/n): ", end='')
    response = input().strip().lower()

    if response != 'y':
        print("キャンセルしました。")
        return

    print()

    # 各ファイルを処理
    for idx, item in enumerate(processing_data, 1):
        file_name = item['file_name']
        file_id = item['file_id']
        local_path = item['local_path']

        print(f"[{idx}/{len(processing_data)}] 処理中: {file_name}")

        # ローカルファイルを削除
        if os.path.exists(local_path):
            try:
                os.remove(local_path)
                print(f"  ローカルファイルを削除: {local_path}")
            except Exception as e:
                print(f"  ローカルファイル削除エラー: {str(e)}")

        # Google Driveでファイルを移動
        try:
            move_file_to_folder(file_id, config.PROCESSED_FOLDER_ID)
            print(f"  Driveファイルを移動: {file_name} → 読み取り済データ")
        except Exception as e:
            print(f"  Driveファイル移動エラー: {str(e)}")

    # 一時ディレクトリを削除（空の場合）
    if os.path.exists(TEMP_PDF_DIR) and not os.listdir(TEMP_PDF_DIR):
        os.rmdir(TEMP_PDF_DIR)
        print(f"\n一時ディレクトリを削除: {TEMP_PDF_DIR}")

    # メタデータファイルを削除
    if os.path.exists(PROCESSING_DATA_FILE):
        os.remove(PROCESSING_DATA_FILE)
        print(f"メタデータファイルを削除: {PROCESSING_DATA_FILE}")

    # 抽出済みJSONファイルを削除
    if os.path.exists(EXTRACTED_JSON_FILE):
        os.remove(EXTRACTED_JSON_FILE)
        print(f"抽出済みJSONファイルを削除: {EXTRACTED_JSON_FILE}")

    print(f"\n{'=' * 60}")
    print("クリーンアップ完了！")
    print(f"{'=' * 60}\n")

def main():
    parser = argparse.ArgumentParser(
        description='PDF名刺情報抽出とスプレッドシートアップロード'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='処理済みファイルのクリーンアップを実行'
    )

    args = parser.parse_args()

    if args.cleanup:
        cleanup_processed_files()
    else:
        prepare_pdfs()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作が中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
