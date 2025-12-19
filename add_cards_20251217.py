"""
スキャン_20251217-0754.pdfから抽出した名刺情報をスプレッドシートに追加
"""
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import append_row_to_sheet

# スキャン_20251217-0754.pdfから抽出した名刺データ
cards = [
    # 1. 濱崎 浩司 - アーストレックロボティクス
    ["濱崎 浩司", "HAMASAKI KOJI", "株式会社アーストレックロボティクス (EARTH TREK)", "CTO", "hamasaki@et-robotics.co.jp", "", "0120-72-3788", "", "550-0011", "大阪市西区阿波座2-2-18 NANKAI 西本町ビル 11F", "https://et-robotics.co.jp", "", "", "", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 2. 吉田周司 - delight design
    ["吉田周司", "", "delight design", "", "", "", "", "", "", "", "", "", "", "d-fab", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 3. 溝口 聡志 - Gallery Goro
    ["溝口 聡志", "Satoshi Mizoguchi", "Gallery Goro", "アートイベントディレクター 企画部長", "s.mizoguchi@g-goro.co.jp", "", "06-6964-5656", "", "536-0014", "大阪市城東区鴫野西2-19-9 川崎ビル (JR京橋駅南口徒歩10分)", "", "", "", "額縁・アートイベントのギャラリーゴロー", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 4. 梨本 紅美 - 梨の木行政書士事務所
    ["梨本 紅美", "Nashimoto Kumi", "梨の木行政書士事務所", "代表 行政書士", "nashinoki.nashimoto@gmail.com", "", "075-600-0562", "", "604-8118", "京都府京都市中京区堺町通三条下ゝ乙道祐町141 I.B-Office4階416号室", "", "", "", "", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 5. 岩崎義弘 - PPnR inc.
    ["岩崎義弘", "", "PPnR inc.", "ウェブディレクター、生成AI", "iwasaki@ppnr.co.jp", "090-2117-7374", "", "", "", "", "", "", "", "", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 6. 坂口 元哉 - NexConVentures
    ["坂口 元哉", "Genya Sakaguchi", "株式会社 NexConVentures", "代表取締役", "sakaguchi@nexconventures.com", "080-3036-9547", "", "", "531-0072", "大阪市北区豊崎3丁目4-14 ショーレイビル 507/508", "", "", "", "派-27-305409 27-ユ-304637", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 7. 畠山 和己 - シャムロック顕至
    ["畠山 和己", "", "シャムロック顕至", "代表", "info@yume-kikiyose.com", "", "", "", "", "", "https://yume-kikiyose.com", "", "", "占い師・産業カウンセラー", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 8. 越前 多恵子 - SUNITED
    ["越前 多恵子", "Taoko Echizen", "SUNITED 株式会社", "総合営業部 西日本統括アネージャー・ソリューションコーディネーター", "echizen-taoko@sunited.co.jp", "080-4714-5720", "03-6268-9503", "", "600-8449", "京都市下京区新町通松原下る富永町107番地1 GROVING BASE", "https://sunited.co.jp/", "", "", "本社: 〒102-0083 東京都千代田区麹町2-5-1 半蔵門PREX South 6F", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 9. 畑 裕之 - ホウバイ
    ["畑 裕之", "Hiroyuki hata", "株式会社ホウバイ", "代表取締役", "hata@houbai.co.jp", "090-3353-2998", "", "", "532-0012", "大阪市淀川区木川東3-9-10-304", "https://houbai.co.jp", "", "", "Microsoft CSPパートナー おもてなし規格認証 審査員", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 10. 和佐 周治 - 和佐塾
    ["和佐 周治", "Shuji Wasa", "合同会社 和佐塾 (Wasa Juku, LLC)", "代表", "info@wasajuku.com", "", "06-6133-5487", "", "530-0001", "大阪府大阪市北区梅田2-2-2 ヒルトンプラザウエスト19階", "https://wasajuku.com", "", "", "", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 11. 黒岡 伸行 - 生成AIサポーター
    ["黒岡 伸行", "そらおは", "", "生成AIサポーター", "kroknbyk@gmail.com", "09083676213", "", "", "", "", "", "", "LINE公式, Facebook, Instagram", "AI個別サポート, Chat GPT講座, 画像生成講座, その他各種AI講座, LINEスタンプ作成, AIアバター作成, AI動画作成, GPTs作成, 機械設計コンサル", "スキャン_20251217-0754.pdf", datetime.now().strftime("%Y-%m-%d")],
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
