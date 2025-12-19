"""
名刺情報をスプレッドシートに追加するスクリプト
"""
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import append_row_to_sheet

# 名刺情報
card_data = [
    "陳麒安",  # 氏名(漢字)
    "Augustine Chen (チン チアン)",  # 氏名(ローマ字)
    "達明機器人股份有限公司 (TECHMAN ROBOT INC.)",  # 会社名
    "専案経理 日本業務部 Program Manager Japan Sales Department",  # 役職
    "augustine.chen@tm-robot.com",  # メールアドレス
    "+886 937 088 184",  # 携帯電話
    "+886 3 328 8350",  # 固定電話
    "+886 3 327 7220",  # FAX
    "33383",  # 郵便番号
    "桃園市亀山区華亜二路58-2號5楼, Taiwan",  # 住所
    "https://www.tm-robot.com",  # ウェブサイト
    "",  # LINE ID
    "",  # その他SNS
    "TM名古屋支店: 〒461-0001 名古屋市東区泉2-21-28 日刊工業新聞社名古屋支社ビル5F -501号室",  # 備考
    "スキャン_20251030-0852.pdf",  # スキャンファイル名
    datetime.now().strftime("%Y-%m-%d")  # 読み取り日
]

# スプレッドシートに追加
result = append_row_to_sheet(config.SPREADSHEET_ID, card_data)
try:
    print(f"追加完了: {card_data[0]} ({card_data[2]})")
except UnicodeEncodeError:
    print(f"追加完了: カード追加成功")
print(f"更新範囲: {result.get('updates', {}).get('updatedRange', 'N/A')}")
