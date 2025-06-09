# 🌸 LINE Voice Bot — 寧心雪語音回覆系統

這是一個使用 Flask 架構的 LINE 機器人，能夠自動回覆使用者的文字訊息為語音。  
語音由 [gTTS](https://pypi.org/project/gTTS/) 生成，並透過 [file.io](https://www.file.io/) 短期託管給 LINE 播放。

---

## 🚀 功能說明

- 接收 LINE 使用者的文字訊息
- 將文字轉換為中文語音（gTTS）
- 將語音上傳至 file.io 取得公開連結
- 回傳語音訊息至用戶 LINE 聊天視窗

---

## 🛠️ 環境需求

- Python 3.8+
- Flask
- line-bot-sdk
- gTTS
- requests
- python-dotenv

安裝套件：

```bash
pip install -r requirements.txt
```

---

## 📂 環境變數設定

請在專案根目錄建立 `.env` 或於部署平台設定以下變數：

- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`

---

## 🧪 本機測試

```bash
python main.py
```

搭配 [ngrok](https://ngrok.com/) 測試 webhook：

```bash
ngrok http 5000
```

---

## 🧾 部署平台建議

- [Render](https://render.com/)
- [Railway](https://railway.app/)

---

## 🙋 作者

由使用者與 ChatGPT 共同建構  
語音角色靈魂命名為：「寧心雪」
