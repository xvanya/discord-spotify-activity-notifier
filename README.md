# Discord Spotify Activity Notifier 🎵

A Discord bot that tracks a specific user's Spotify activity and sends **direct messages (DMs)** when:
- the user starts listening to a song
- the song changes
- the user stops listening to Spotify

The bot is designed to be **stable**, **spam-free**, and reliable even though Discord may emit multiple presence update events.

---

## ✨ Features

- 🎧 Detects Spotify listening activity via Discord presence
- 📩 Sends notifications directly to Discord DMs
- 🧠 Smart debounce & anti-duplicate logic
- 🔐 Uses `.env` for secure token storage
- 🖥️ Console logging for debugging
- ✅ Compatible with Python 3.12+

---

## 🛠️ Requirements

- Python **3.10+** (tested on 3.12)
- A Discord bot with **Presence Intent enabled**
- Libraries:
  - `discord.py`
  - `python-dotenv`

---

## 🚀 Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
