import requests
import threading
import random

candidate_map = {1: "ネオバタくん", 2: "レーズンさん", 3: "黒糖どん", 4: "全粒くん", 5: "ライ麦くん", 6: "豆乳ちゃん", 7: "米粉さん", 8: "フランス・ロール三世"}
genders = ["男性", "女性", "未回答"]
ages = ["10代以下", "20代", "30代", "40代", "50代", "60代以上"]
prefectures = ["北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県", "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県", "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"]

def vote(candidate_name):
    session = requests.Session()
    try:
        token_resp = session.get("https://www.fujipan.co.jp/product/neo/neobatakun/vote/get_token.php")
        token_resp.raise_for_status()
        token = token_resp.json()["token"]
    except Exception as e:
        print(f"[❌] Get Token Failed\n{e}")
        return
    gender = random.choice(genders)
    age = random.choice(ages)
    location = random.choice(prefectures)
    form_data = {"token": token, "choice": candidate_name, "gender": gender, "age_group": age, "location": location}
    try:
        res = session.post("https://www.fujipan.co.jp/product/neo/neobatakun/vote/vote.php", data=form_data)
        if res.status_code == 200:
            print(f"[⭕️] Vote Succeeded\n{token} - {candidate_name} ({gender}, {age}, {location})")
        else:
            print(f"[❌] Vote Failed\nStatus Code: {res.status_code}")
    except Exception as e:
        print(f"[❌] Vote Error\n{e}")

def run_votes(candidate_number, count):
    if candidate_number not in candidate_map:
        print("[❌] Invalid Candidate Number")
        return
    candidate_name = candidate_map[candidate_number]
    threads = []
    for _ in range(count):
        t = threading.Thread(target=vote, args=(candidate_name,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print("[✅] All Votes Completed")

if __name__ == "__main__":
    print("[🔢] Candidate List\n1: ネオバタくん\n2: レーズンさん\n3: 黒糖どん\n4: 全粒くん\n5: ライ麦くん\n6: 豆乳ちゃん\n7: 米粉さん\n8: フランス・ロール三世")
    candidate = input("[❓] Candidate Number: ")
    count = input("[❓] How Many Votes: ")
    run_votes(candidate_number=int(candidate), count=int(count))
