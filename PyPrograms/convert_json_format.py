"""
抽出したJSONを add_cards_batch.py が期待する形式に変換するスクリプト
"""

import json
import sys
from datetime import datetime

def convert_json_format(input_file, output_file):
    """
    抽出したJSONファイルをadd_cards_batch.py用の形式に変換

    Args:
        input_file: 入力JSONファイルパス
        output_file: 出力JSONファイルパス
    """
    # JSONファイルを読み込み
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 変換後のデータを格納
    cards = []

    for item in data:
        # 各項目を配列に変換（スプレッドシートの列順に合わせる）
        card = [
            item.get('氏名(漢字)', ''),
            item.get('氏名(ローマ字)', ''),
            item.get('会社名', ''),
            item.get('役職', ''),
            item.get('メールアドレス', ''),
            item.get('携帯電話', ''),
            item.get('固定電話', ''),
            item.get('FAX', ''),
            item.get('郵便番号', ''),
            item.get('住所', ''),
            item.get('ウェブサイト', ''),
            item.get('LINE ID', ''),
            item.get('その他SNS', ''),
            item.get('備考', ''),
            item.get('filename', ''),  # スキャンファイル名
            datetime.now().strftime("%Y-%m-%d")  # 読み取り日
        ]
        cards.append(card)

    # 出力形式に変換
    output_data = {
        "source_pdf": "一括登録",  # 複数のPDFから抽出した場合
        "cards": cards
    }

    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"変換完了: {len(cards)}件の名刺データを変換しました")
    print(f"出力ファイル: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python convert_json_format.py <入力JSONファイル> [出力JSONファイル]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "converted_cards.json"

    convert_json_format(input_file, output_file)
