"""
Business Card Management System - Main CLI
Provides a menu interface for common operations
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_menu():
    """メインメニューを表示"""
    print("\n" + "="*60)
    print("名刺管理システム - Business Card Management System")
    print("="*60)
    print("\n利用可能な操作:")
    print("  1. Google Driveフォルダ内の全ファイルをリスト")
    print("  2. PDFファイルのみをリスト")
    print("  3. GoogleスプレッドシートからCLAUDE.mdを生成")
    print("  4. PDFファイルをダウンロード")
    print("  5. PDF処理準備（名刺情報抽出用にダウンロード）")
    print("  6. 処理済みPDFのクリーンアップ")
    print("  7. JSONファイルから名刺を一括追加")
    print("  8. 終了")
    print("\n" + "="*60)

def main():
    """メイン処理"""
    while True:
        show_menu()
        choice = input("\n操作を選択してください (1-8): ").strip()

        if choice == '1':
            print("\n[Google Driveフォルダの内容をリスト中...]")
            import inspect_drive
            inspect_drive.main()

        elif choice == '2':
            print("\n[PDFファイルをリスト中...]")
            import list_pdfs
            list_pdfs.main()

        elif choice == '3':
            print("\n[CLAUDE.mdを生成中...]")
            import create_claude_md_from_sheet
            create_claude_md_from_sheet.main()

        elif choice == '4':
            print("\n[PDFダウンロード]")
            import download_pdf
            download_pdf.main()

        elif choice == '5':
            print("\n[PDF処理準備]")
            import extract_and_upload_to_sheet
            extract_and_upload_to_sheet.prepare_pdfs()

        elif choice == '6':
            print("\n[処理済みPDFのクリーンアップ]")
            import extract_and_upload_to_sheet
            extract_and_upload_to_sheet.cleanup_processed_files()

        elif choice == '7':
            print("\n[JSONファイルから名刺を一括追加]")
            import add_cards_batch
            add_cards_batch.main()

        elif choice == '8':
            print("\n終了します。")
            break

        else:
            print("\n無効な選択です。1-8の数字を入力してください。")

        # 続行確認
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            input("\nEnterキーを押してメニューに戻る...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作が中断されました。")
        sys.exit(0)
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        sys.exit(1)
