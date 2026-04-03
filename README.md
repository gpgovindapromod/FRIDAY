<div align="center">

# 🤖 FRIDAY AI
### Next-Generation Intelligent Voice Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> *Your intelligent companion for voice, automation, and data — built for the future, ready today.*

</div>

---

## ✨ Features

## Features Overview

| Category               | Capabilities                                                                 |
|------------------------|------------------------------------------------------------------------------|
| 🎤 **Voice Commands** | In-browser speech recognition (Web Speech API)                               |
| 🌤️ **Weather**        | Real-time weather by city or auto-detected location                          |
| 📝 **Notes & Tasks**  | Save notes and manage to-do lists (SQLite)                                   |
| 💰 **Finance**        | Live stock prices (via yfinance) & crypto prices                             |
| 🔍 **Search**         | Google search & Wikipedia summaries                                          |
| 📖 **Dictionary**     | Word definitions and meanings                                                |
| 🖥️ **System Info**    | CPU, RAM, disk usage via psutil                                              |
| 🔐 **Security Tools** | Secure password generator, SHA-256/MD5 hashing                               |
| 🎮 **Fun**            | Jokes, dice roll, coin flip, random numbers                                  |
| 🎬 **Entertainment**  | Movie info (OMDB), Spotify search                                            |

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask, Flask-CORS
- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **Database:** SQLite (`friday_data.db`)
- **APIs:** OpenWeatherMap, CoinGecko, OMDB, ExchangeRate
- **Fonts:** Orbitron + Syne (Google Fonts)

---

## 📁 Project Structure

```
friday-ai/
├── app.py                  # Flask backend & API routes
├── Features1.py            # Web search, weather, Wikipedia
├── Automations1.py         # Dictionary, reminders, sentiment
├── Enhanced_Features.py    # Finance, system, notes, tasks, fun
├── templates/
│   ├── index.html          # Landing page
│   └── dashboard.html      # AI chat dashboard
├── Procfile                # For Render/Heroku deployment
├── requirements.txt        # Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/friday-ai.git
cd friday-ai
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your API key (optional)
```bash
# Windows
set OPENWEATHER_API_KEY=your_api_key_here

# macOS/Linux
export OPENWEATHER_API_KEY=your_api_key_here
```
> Get a free key at [openweathermap.org](https://openweathermap.org/api)

### 5. Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 💬 Example Commands

```
"What's the weather today?"
"Tell me a joke"
"What time is it?"
"Search Google for Python tutorials"
"Stock price of AAPL"
"Crypto price of bitcoin"
"Save note Buy groceries tomorrow"
"Show my tasks"
"Add task Finish the report"
"Generate password"
"System information"
"Who is Elon Musk?"
"Define serendipity"
```

---

## ☁️ Deploying to Render (Free)

1. Push this repo to GitHub
2. Sign up at [render.com](https://render.com)
3. **New → Web Service → Connect your repo**
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. Click **Deploy** 🎉

> **Note:** Voice output (TTS) and microphone features depend on the browser's Web Speech API. They work on Chrome/Edge.

---

## ⚠️ Cloud Limitations

Some features are designed for local use only and are gracefully disabled on cloud:

- `pyttsx3` — requires system audio
- `PyAudio` — requires microphone hardware  
- `pyautogui` — requires a desktop screen
- `selenium` — requires a browser driver

All other features (chat, weather, finance, notes, etc.) work normally in the cloud.

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ | Powered by Flask & Web Speech API

</div>
