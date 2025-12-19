"""
複数の名刺情報をまとめてスプレッドシートに追加
"""
import sys
import os
from datetime import datetime

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyPrograms import config
from PyPrograms.utils import append_row_to_sheet

# スキャン_20251026-0810.pdfから抽出した名刺データ
cards = [
    # 1. 土橋 勉 - LIMNO
    ["土橋 勉", "TSUTOMU DOBASHI", "株式会社LIMNO", "取締役 常務執行役員", "dobashi.tsutomu@limno.co.jp", "070-8701-7466", "0857-21-2047", "0857-21-2621", "680-8634", "鳥取県鳥取市立川町7丁目101番地", "", "", "", "東京本社: 150-0011 東京都渋谷区東1丁目29番3号", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 2. 山田 克基 - Blooming Camp
    ["山田 克基", "Katsuki Yamada", "Blooming Camp", "コミュニティマネージャー", "bloomingcamp-info-ml@sakura.ad.jp", "", "", "", "530-0011", "大阪市北区大深町6番38号 グラングリーン大阪 北館 JAM BASE 3階", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 3. 清水 綱之 - オリックス
    ["清水 綱之", "", "オリックス株式会社", "大阪事業法人営業第一部 第一チーム長", "tsunayuki.shimizu.cd@orix.jp", "080-1245-1263", "06-6578-1667", "06-6578-1695", "550-0005", "大阪府大阪市西区西本町1-4-1 オリックス本町ビル", "https://www.orix.co.jp", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 4. 西田 崇人 - セーフィー
    ["西田 崇人", "", "セーフィー株式会社", "GL 営業本部 関西支店 関西営業グループ", "t-nishida@safie.jp", "080-4784-8703", "", "", "530-0011", "大阪府大阪市北区大深町6 38 グラングリーン大阪 北館 JAM BASE 6階 JAM-OFFICE 6-A", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 5. 大城 由佳 - コングレス
    ["大城 由佳", "OSHIRO Yuka", "コングレスクエア グラングリーン大阪", "", "yuka-oshiro@congre.co.jp", "", "06-6292-6047", "", "530-0011", "大阪市北区大深町5-54 グラングリーン大阪 南館4F", "https://osaka.congres-square.jp/grandgreen/", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 6. 青海 亮兵 - ハートフルサンク
    ["青海 亮兵", "", "株式会社ハートフルサンク", "ディサービスカンパニー社長、医療住環境カンパニー長、ひしき乃湯管理者", "", "080-7258-8308", "", "", "593-8315", "大阪府堺市西区菱木1丁2446番地の1土井ビル1階", "", "", "", "事業所番号: 2776302537 ハートフルサンク デイ・ひしき乃湯, 2756320202 ハートフルサンク デイ・ひしき乃池, 2716301433 ハートフルサンク デイ・ひしき乃湯(生活訓練課後等デイサービス)", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 7. 和佐 周治 - 合同会社和佐塾
    ["和佐 周治", "Shuji Wasa", "合同会社和佐塾", "代表", "", "", "06-6133-5487", "", "530-0001", "大阪府大阪市北区梅田2-2-2 ヒルトンプラザウエスト19階", "https://wasajuku.com", "", "info@wasajuku.com", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 8. ジョセフ ポーティン - ブレーンパワー
    ["ジョセフ ポーティン", "JOSEPH PORTIN", "株式会社ブレーンパワー", "営業部 外国語教育推進課 教育開発グループ スーパーバイザー", "joseph@brain-power.jp", "080-6108-8600", "050-5799-1928", "050-3527-0855", "530-0011", "大阪府大阪市北区大深町6-38 グラングリーン大阪 北館 JAM BASE 3F", "https://www.brain-power.co.jp", "", "", "YouTube: BrainPower-Osakaチャンネル", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 9. 山田 克基 - 燈スタジオ
    ["山田 克基", "Katsuki Yamada", "燈スタジオ (AKARI STUDIO)", "コニー", "yamada@akaristudio.jp", "080-6118-4738", "", "", "", "", "", "", "X: @coney_pr", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 10. 村上 莉奈 - every
    ["村上 莉奈", "", "株式会社every", "", "r.murakami@teamenergy.co.jp", "070-1521-1116", "", "", "", "大阪市中央区北浜2丁目6-18 淀屋橋スクエア15階 (大阪オフィス)", "", "", "info@every-every.com", "東京都新宿区内藤町1-82ブルニエ (東京オフィス)", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 11. 石川 真太郎 - イグニション・ポイント
    ["石川 真太郎", "", "イグニション・ポイント株式会社", "コンサルティング事業本部 デジタルユニット シニアコンサルタント", "shintaro.ishikawa@ignitionpoint-inc.com", "", "06-6131-4601", "", "530-0011", "大阪府大阪市北区大深町 6-38 グラングリーン大阪北館 JAM BASE3 階", "https://ignitionpoint-inc.com", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 12. 堀川 幸裕 - 日東電工
    ["堀川 幸裕", "", "日東電工株式会社", "常務執行役員 経営特命執行責任", "yukihiro.horikawa@nitto.com", "080-1179-3245", "06-7632-2101", "", "530-0011", "大阪市北区大深町4番20号 グランフロント大阪タワーA 33階", "https://www.nitto.com/jp/ja/", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 13. 中 綾子 - 映像ディレクター/スタイリスト
    ["中 綾子", "", "", "映像ディレクター | スタイリスト", "visualcolor1301@gmail.com", "", "", "", "", "", "", "", "", "映像制作: ブランディングムービー、SNSショートムービー、サイネージムービー / スタイリスト: ファッションスタイリスト、パーソナルカラーリスト", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 14. 山内 翔貴 - AVITA
    ["山内 翔貴", "Shoki Yamauchi", "AVITA", "アバタービジネス局 / パートナーサクセス部 インサイドセールス", "yamauchi@avita.co.jp", "070-5567-0438", "", "", "153-0064", "東京都目黒区下目黒1丁目8-1 アルコタワー 18 階", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 15. 鈴山 佳宏 - RAYVEN
    ["鈴山 佳宏", "SUZUYAMA YOSHIHIRO", "株式会社RAYVEN", "代表取締役", "s.yoshihiro@rayven.cloud", "070-8437-9586", "", "", "", "", "www.rayven.cloud/", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 16. 中村 康宏 - アナザーブレイン税理士事務所
    ["中村 康宏", "Nakamura Yasuhiro", "アナザーブレイン税理士事務所", "税理士・CFP®", "nakamura@anotherbrain-tax.com", "", "090-9713-7266", "", "531-0076", "大阪府大阪市北区大淀中1-8-27", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 17. 趙 陽 - 銘洋貿易
    ["趙 陽", "", "銘洋貿易株式会社", "代表取締役", "cyouyou@mingyang826.com", "080-3571-6886", "072-395-6839", "072-395-6840", "574-0011", "大阪府大東市北条7-15-33", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 18. 近藤 綾香 - ヘルスケアサーカス
    ["近藤 綾香", "Ayaka Kondo", "ヘルスケアサーカス株式会社", "代表取締役 薬剤師", "ayaka.kondo@healthcarecircus.co.jp", "080-6336-1485", "", "", "", "", "", "", "", "症状軸の患者コミュニティ プラットフォーム", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 19. 長谷川 美澄 - フリーライター
    ["長谷川 美澄", "Mizuki Hasegawa", "", "フリーライター", "", "", "", "", "", "", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 20. 木村 彰利 - オリックス・キャピタル
    ["木村 彰利", "", "オリックス・キャピタル株式会社", "シニアヴァイスプレジデント", "akitoshi.kimura.dg@orix.jp", "080-8028-3458", "03-3435-3330", "", "105-5135", "東京都港区浜松町2-4-1 世界貿易センタービル南館", "https://orixcapital.co.jp", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 21. 西岡 輝樹 - スクエアプラス
    ["西岡 輝樹", "", "株式会社スクエアプラス", "BANTO Business achievements navigation total officer", "t-nishioka@square-plus.com", "080-4637-3611", "06-4304-5554", "06-6765-5559", "542-0061", "大阪市中央区安堂寺町1丁目5-12 第2近宣ビル1F", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 22. 木下 稔 - CLEAIR
    ["木下 稔", "", "株式会社CLEAIR", "取締役", "info@cleair-w.com", "090-1132-7465", "06-6258-3880", "06-6258-3890", "542-0061", "大阪市中央区安堂寺町1丁目5-12", "", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 23. 林 秀紀 - CHU-HI BAR frank
    ["林 秀紀", "Hideki hayashi", "CHU-HI BAR frank", "", "", "050-1721-4488", "", "", "650-0011", "兵庫県神戸市中央区下山手通1丁目5-7 東門ウエストコート2F", "", "", "Instagram、LINE", "月~木 18:00-23:00, 金~土 18:00-LAST, 日・祝 定休日", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 24. Yuuma - Star Blazers (ドローンサッカー)
    ["Yuuma", "", "Star Blazers (Saiworks Yokohama)", "", "yuuma.22.dronesoccer@gmail.com", "", "", "", "", "", "", "", "Instagram: @YUUMA.15.02.22", "Japan Team, World Cup Team, Class40 Position Striker, Class20 Position Striker", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 25. 髙品 悟 - オリックス
    ["髙品 悟", "", "オリックス株式会社", "大阪事業法人営業第一部 第一チーム長 事業承継・M&Aエキスパート", "satoru.takashina.jg@orix.jp", "080-3392-8884", "06-6578-1667", "06-6578-1695", "550-0005", "大阪府大阪市西区西本町1-4-1 オリックス本町ビル", "https://www.orix.co.jp", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],

    # 26. Grant Hill - Drone Soccer Association (AUSTRALIA)
    ["Grant Hill", "", "Drone Soccer Association", "President", "grant@dronesoccerassociation.com", "+61 4359 54321", "", "", "", "AUSTRALIA", "www.dronesoccerassociation.com", "", "", "", "スキャン_20251026-0810.pdf", datetime.now().strftime("%Y-%m-%d")],
]

# 各名刺をスプレッドシートに追加
for i, card in enumerate(cards, 1):
    try:
        result = append_row_to_sheet(config.SPREADSHEET_ID, card)
        print(f"[{i}/{len(cards)}] 追加完了: {card[0]} ({card[2]})")
    except Exception as e:
        print(f"[{i}/{len(cards)}] エラー: {card[0]} - {str(e)}")

print(f"\n合計{len(cards)}件の名刺を処理しました。")
