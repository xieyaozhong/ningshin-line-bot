# 寧心雪 LINE 語音助手
# 建立一個簡單的 Flask 應用，接收 LINE 訊息並透過 OpenAI 語音 API 回傳語音

from flask import Flask, request, abort, send_file
from io import BytesIO
import openai
import requests
import os

app = Flask(__name__)

# === 設定區 ===
CHANNEL_ACCESS_TOKEN = "hxUFQfFxtfz/d54PHXNiLnapiTaRmBjyMYzeeUhzI4BZF8/sSiFSfV+SVOunurTc4jKvY/ZgbhvjqITjho604IYLz8SkC9l8G7zWuSLnPnC6q6rCY6Hs/GoNeQmEvN9+5pZh+svlwK+JEC9UEtWS+AdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "f6729885cc7fd58fe025bc0ef424709f"
openai.api_key = os.getenv("OPENAI_API_KEY")  # 在部署環境中設好 OPENAI_API_KEY 環境變數

LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
}

def generate_voice(text: str) -> BytesIO:
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    mp3_bytes = BytesIO(response.content)
    return mp3_bytes

def upload_audio_to_line(audio_bytes: BytesIO) -> str:
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "audio/mpeg"
    }
    audio_bytes.seek(0)
    response = requests.post("https://api-data.line.me/v2/bot/richmenu/content", headers=headers, data=audio_bytes)
    return response.json()

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_json()

    if "events" not in body:
        return "ok"

    for event in body["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_text = event["message"]["text"]
            reply_token = event["replyToken"]

            voice = generate_voice(user_text)

            # LINE 不允許直接上傳音訊給 reply API，只能回傳 audio message
            audio_message = {
                "type": "audio",
                "originalContentUrl": "https://yourserver.com/static/voice.mp3",
                "duration": 2000
            }
            requests.post(LINE_REPLY_URL, headers=HEADERS, json={
                "replyToken": reply_token,
                "messages": [audio_message]
            })

            # 同時將語音存檔（方便下載或測試）
            with open("static/voice.mp3", "wb") as f:
                f.write(voice.read())

    return 'OK'

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(host='0.0.0.0', port=5000)

