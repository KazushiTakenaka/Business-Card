"""
JSONファイルから名刺データを読み込み、スプレッドシートに一括追加するスクリプト

使用方法:
1. 名刺データをJSONファイルに保存
2. このスクリプトを実行してJSONファイルを指定
3. スプレッドシートに一括追加

JSONファイル形式:
{
  "source_pdf": "スキャン_20251217-0754.pdf",
  "cards": [
    ["氏名", "ローマ字", "会社名", "役職", "メール", "携帯", "固定電話", "FAX", "郵便番号", "住所", "ウェブサイト", "LINE ID", "その他SNS", "備考"],
    ["氏名2", "ローマ字2", "会社名2", ...]
  ]
}
"""

import sys
import os
import json
import argparse
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import append_row_to_sheet

def load_cards_from_json(json_file_path):
    """
    JSONファイルから名刺データを読み込む

    Args:
        json_file_path: JSONファイルのパス

    Returns:
        tuple: (source_pdf, cards) - PDFファイル名と名刺データのリスト
    """
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    source_pdf = data.get('source_pdf', '')
    cards = data.get('cards', [])

    # 各カードにスキャンファイル名と読み取り日を追加
    processed_cards = []
    current_date = datetime.now().strftime("%Y-%m-%d")

    for card in cards:
        # カードデータが14列の場合、スキャンファイル名と読み取り日を追加
        if len(card) == 14:
            card.append(source_pdf)
            card.append(current_date)
        # 16列の場合はそのまま使用
        elif len(card) == 16:
            pass
        else:
            print(f"警告: カードデータの列数が不正です（{len(card)}列）。スキップします。")
            continue

        processed_cards.append(card)

    return source_pdf, processed_cards

def add_cards_to_sheet(cards, source_pdf=""):
    """
    複数の名刺をスプレッドシートに追加

    Args:
        cards: 名刺データのリスト
        source_pdf: PDFファイル名（ログ出力用）

    Returns:
        tuple: (成功数, 失敗数)
    """
    success_count = 0
    error_count = 0

    for i, card in enumerate(cards, 1):
        try:
            result = append_row_to_sheet(config.SPREADSHEET_ID, card)

            # 名前と会社名を取得（インデックスエラーを避ける）
            name = card[0] if len(card) > 0 else "不明"
            company = card[2] if len(card) > 2 else ""

            try:
                if company:
                    print(f"[{i}/{len(cards)}] 追加完了: {name} ({company})")
                else:
                    print(f"[{i}/{len(cards)}] 追加完了: {name}")
            except UnicodeEncodeError:
                print(f"[{i}/{len(cards)}] 追加完了")

            success_count += 1

        except Exception as e:
            error_count += 1
            try:
                print(f"[{i}/{len(cards)}] エラー: {name} - {str(e)}")
            except UnicodeEncodeError:
                print(f"[{i}/{len(cards)}] エラー: {str(e)}")

    return success_count, error_count

def main():
    parser = argparse.ArgumentParser(
        description='JSONファイルから名刺データを読み込み、スプレッドシートに追加'
    )
    parser.add_argument(
        'json_file',
        nargs='?',
        help='名刺データを含むJSONファイルのパス'
    )

    args = parser.parse_args()

    # JSONファイルが指定されていない場合は対話的に入力
    if not args.json_file:
        print("JSONファイルのパスを入力してください:")
        json_file_path = input().strip()
    else:
        json_file_path = args.json_file

    # ファイルの存在確認
    if not os.path.exists(json_file_path):
        print(f"エラー: ファイルが見つかりません: {json_file_path}")
        sys.exit(1)

    print("=" * 60)
    print("名刺データ一括追加")
    print("=" * 60)
    print()

    # JSONファイルを読み込み
    try:
        source_pdf, cards = load_cards_from_json(json_file_path)
    except Exception as e:
        print(f"エラー: JSONファイルの読み込みに失敗しました: {str(e)}")
        sys.exit(1)

    if not cards:
        print("エラー: 名刺データが見つかりません。")
        sys.exit(1)

    print(f"読み込み元PDF: {source_pdf}")
    print(f"名刺データ数: {len(cards)}件")
    print()

    # 確認
    print("スプレッドシートに追加しますか？ (y/n): ", end='')
    response = input().strip().lower()

    if response != 'y':
        print("キャンセルしました。")
        sys.exit(0)

    print()

    # スプレッドシートに追加
    success_count, error_count = add_cards_to_sheet(cards, source_pdf)

    # 結果サマリー
    print()
    print("=" * 60)
    print(f"処理完了: 成功 {success_count}件, エラー {error_count}件")
    print("=" * 60)

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
