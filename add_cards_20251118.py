"""
スキャン_20251118-1425.pdfから抽出した名刺情報をスプレッドシートに追加
"""
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import append_row_to_sheet

# スキャン_20251118-1425.pdfから抽出した名刺データ
cards = [
    # 1. 菱川 陽亮 - RIDE AD AGENCY
    ["菱川 陽亮", "YOSUKE HISHIKAWA", "株式会社 RIDE AD AGENCY", "代表取締役 / フォトグラファー・映像ディレクター", "hishikawaphoto@gmail.com", "080-6147-4321", "06-7777-1169", "", "533-0023", "大阪府大阪市東淀川区東淡路1-5-3-829", "https://ridecorp.myportfolio.com", "", "Instagram: ride.photographer", "", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 2. 井坂 浩章 - Classmate
    ["井坂 浩章", "Hiroaki Isaka", "Classmate株式会社", "代表取締役社長 / CEO", "h_isaka@cne1classmate.com", "090-6919-3477", "", "", "590-0077", "大阪府堺市堺区中瓦町1-4-22 大阪信用金庫堺東ビル2F", "http://www.classmatejp.com", "", "", "OPEN WORLD THROUGH EDUCATION", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 3. 松尾 としき - AiX Group
    ["松尾 としき", "Toshiki Matsuo", "AiX Group (エーアイクロス グループ)", "代表", "t.matsuo@aixg.jp", "", "", "", "", "", "https://aixg.jp", "", "Facebook: https://facebook.com/matsuotoshiki", "", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 4. 大西 紘平 - 合通ホールディングス
    ["大西 紘平", "", "合通ホールディングス株式会社 (GOTSU)", "G.L.C. 課長", "kohei_ohnishi@gotsu.co.jp", "070-3133-3572", "06-6458-1300", "06-6458-7121", "553-0002", "大阪府大阪市福島区鷺洲4丁目1番16号", "https://www.gotsu.co.jp", "", "", "", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 5. 井上 和茂 - いのうえ技術経営事務所
    ["井上 和茂", "INOUE Kazushige", "いのうえ技術経営事務所", "中小企業診断士、技術士（電気電子部門）、エネルギー管理士（熱・電気）、第1種電気主任技術者、健康経営エキスパートアドバイザー", "kinoue@ab.auone-net.jp", "080-6787-3448", "", "", "663-8124", "兵庫県西宮市小松南町 3-4-11-207", "", "", "", "", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 6. 船見 信道 - 気象工学研究所
    ["船見 信道", "", "株式会社 気象工学研究所 (MEC - 関西電力グループ)", "営業グループ 課長代理 気象予報士・防災士", "funami.nobumichi@meci.jp", "", "06-6441-1022", "06-6441-1050", "550-0003", "大阪市西区京町堀1丁目8番5号", "", "", "", "予報業務許可事業者 第88号", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 7. 泉 款太 - SalesDock
    ["泉 款太", "kanta Izumi", "株式会社SalesDock", "代表取締役", "k.izumi@salesdock.jp", "080-7503-8751", "", "", "541-0053", "大阪府大阪市中央区本町4-2-12 野村不動産御堂筋本町ビル 8F", "https://salesdock.jp/", "", "", "", "スキャン_20251118-1425.pdf", datetime.now().strftime("%Y-%m-%d")],
]

# 各名刺をスプレッドシートに追加
for i, card in enumerate(cards, 1):
    try:
        result = append_row_to_sheet(config.SPREADSHEET_ID, card)
        try:
            print(f"[{i}/{len(cards)}] 追加完了: {card[0]} ({card[2]})")
        except UnicodeEncodeError:
            print(f"[{i}/{len(cards)}] 追加完了")
    except Exception as e:
        print(f"[{i}/{len(cards)}] エラー: {str(e)}")

print(f"\n合計{len(cards)}件の名刺を処理しました。")
