# 🌸 寧心雪 LINE Bot

以 Flask + LINE Messaging API + OpenAI Responses API 建立的繁體中文 LINE 對話／語音 Bot。

## 功能

- LINE 文字訊息 webhook
- 寧心雪 AI 對話人格（設定 `OPENAI_API_KEY` 後啟用）
- gTTS 繁中語音回覆
- Bot 自己提供短期 MP3 URL，不依賴 file.io
- 實際偵測 MP3 長度後送給 LINE
- 每位使用者保留目前執行程序內的短期對話上下文
- 陪伴模式、開導模式、認真模式
- 語音開啟／關閉、重置記憶
- Render Blueprint / Gunicorn 部署設定

## 指令

在 LINE 直接輸入：

- `陪伴模式`
- `開導模式`
- `認真模式`
- `語音開啟`
- `語音關閉`
- `重置記憶`
- `功能說明`

## 必要環境變數

```env
LINE_CHANNEL_ACCESS_TOKEN=...
LINE_CHANNEL_SECRET=...
```

若要啟用 AI 對話，再設定：

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5-mini
```

可選：

```env
PUBLIC_BASE_URL=https://your-service.onrender.com
AUDIO_TTL_SECONDS=900
MAX_USER_TEXT=3000
```

> 不要把真實 Token / Secret / API Key 寫進 GitHub。

## 本機執行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

LINE webhook 設為公開 HTTPS 網址的：

```text
https://你的網域/callback
```

## Render

repo 已包含 `render.yaml`。建立 Blueprint 或把現有 Render Web Service 指向 `main` 分支即可。

Build command：

```text
pip install -r requirements.txt
```

Start command：

```text
gunicorn --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT main:app
```

Health check：`/healthz`

## 記憶說明

目前的對話狀態保存在執行中的服務記憶體，因此服務重新啟動或重新部署後會重置。若要做真正跨部署的長期記憶，可再接 PostgreSQL / Redis。

## 安全提醒

這個 repo 過去曾把 LINE Channel Access Token 與 Channel Secret 直接提交到公開 GitHub 歷史。即使目前版本已移除，舊 commit 仍可能看得到，因此應到 LINE Developers 重新發行／更換憑證，並只把新憑證放在部署平台的環境變數中。
