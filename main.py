from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LOSTARK_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDA1OTAzOTYifQ.ete6n3GXirc-kpmuRKS-AvSOMNCyA55VhGUKNflX-ggSCuaw7gq5M8hjsSVNe-UqBNyMAzYrVkye6SdFAOIe70gV3ded6Jg3IQDwK4zd5cqCHmJrvcOdS6iOklRV1Cb4BiM0PW7_YNbPWvUGFaoM77xq5lTNNXAP4K07_hrV_jysppJf7CAfivxorx8F3EmMdkVgkHVbi4kwwKFZRnEJ0M_pgglvkDt2rXpJA-pmw1UE3gB-Dhc_fC1Blo0XJ_iQgFt7Kn2tZhZqRg1LDoDI44cdqiRRQzFG80HEST9Z2DWYwMVkoS7-h4AI_6HIEu2KRS7QFNSQcuQs2Thhx_AW5Q"

def get_character_info(character_name):
    headers = {
        "Authorization": f"bearer {LOSTARK_API_KEY}",
        "Accept": "application/json"
    }
    url = f"https://developer-lostark.game.onstove.com/armory/characters/{character_name}/profiles"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    return None

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    utterance = body.get("userRequest", {}).get("utterance", "")
    character_name = utterance.replace("캐릭터", "").strip()

    if not character_name:
        msg = "캐릭터 이름을 입력해주세요!\n예) 캐릭터 홍길동"
    else:
        info = get_character_info(character_name)
        if info:
            name = info.get("CharacterName", "")
            server = info.get("ServerName", "")
            char_class = info.get("CharacterClassName", "")
            level = info.get("CharacterLevel", "")
            item_level = info.get("ItemAvgLevel", "")
            msg = (
                f"[{server}] {name}\n"
                f"직업: {char_class}\n"
                f"캐릭터 레벨: {level}\n"
                f"아이템 레벨: {item_level}"
            )
        else:
            msg = f"'{character_name}' 캐릭터를 찾을 수 없어요."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": msg}}
            ]
        }
    })

@app.route("/")
def index():
    return "로스트아크 봇 서버 실행 중!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
