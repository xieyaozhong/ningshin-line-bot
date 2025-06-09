from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, AudioSendMessage, TextSendMessage

from gtts import gTTS
import tempfile
import requests
import os

app = Flask(__name__)

# LINE API key（請替換成妳的）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "hxUFQfFxtfz/d54PHXNiLnapiTaRmBjyMYzeeUhzI4BZF8/sSiFSfV+SVOunurTc4jKvY/ZgbhvjqITjho604IYLz8SkC9l8G7zWuSLnPnC6q6rCY6Hs/GoNeQmEvN9+5pZh+svlwK+JEC9UEtWS+AdB04t89/1O/w1cDnyilFU=")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "f6729885cc7fd58fe025bc0ef424709f")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    reply_token = event.reply_token

    # 使用 gTTS 生成語音
    tts = gTTS(text=user_text, lang='zh-tw')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        voice_path = tmp.name
        tts.save(voice_path)

    # 上傳至 file.io，取得公開連結
    with open(voice_path, 'rb') as f:
        response = requests.post("https://file.io/?expires=1d", files={"file": f})
        voice_url = response.json().get("link")

    if voice_url:
        message = AudioSendMessage(
            original_content_url=voice_url,
            duration=4000  # 語音長度（毫秒）
        )
    else:
        message = TextSendMessage(text="語音生成失敗，請稍後再試")

    line_bot_api.reply_message(reply_token, message)

# 可選的健康檢查端點
@app.route("/", methods=["GET"])
def health():
    return "LINE bot is running"

if __name__ == "__main__":
    app.run()
