# 🇲🇹 Welcome To Malta — Telegram Bot with AI + Knowledge Base

A Telegram bot for newcomers and expats in Malta. It answers questions using a knowledge base of PDF files managed by your team, powered by Google Gemini AI.

Made by **devYranzo**

---

## How it works

```
User message via Telegram
     │
     ▼
Gemini AI reads the knowledge base files
     │
     ▼
Answers based only on your documents
     │
     ▼
If topic not found → tells the user honestly
```

The bot never makes up information. Everything it says comes from the PDF files your team uploads to the `knowledge_base/` folder.

---

## Project Structure

```
malta_bot/
├── main.py                  # Bot logic and Telegram handlers
├── context_loader.py        # Reads PDF and TXT files from knowledge_base/
├── requirements.txt         # Python dependencies
├── .env                     # ⚠️ Your secret keys
└── knowledge_base/          # ✏️ Drop your PDFs here
    ├── housing.pdf
    ├── transport.pdf
    ├── health.pdf
    └── general.pdf
```

---

## About this project

This project was developed as part of my internship at **AIntelligence Research**.

The goal was to build a real-world Telegram bot that helps newcomers and expats in Malta by answering questions using a curated knowledge base of PDF documents.

It integrates:
- Telegram Bot API
- Google Gemini AI
- Document-based knowledge retrieval (PDF knowledge base)

---

## Requirements

- Python 3.10 or higher
- A Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- A Google Gemini API Key (from [Google AI Studio](https://aistudio.google.com))

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/devYranzo/WelcomeToMalta-TelegramBot.git
cd WelcomeToMalta-TelegramBot
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Create the `.env` file**

```bash
touch .env
```

Then open `.env` and fill in your keys (see below).

**5. Add your PDF files to `knowledge_base/`**

Drop any PDF there and the bot will use it automatically.

**6. Run the bot**

```bash
python main.py
```

---

## Environment Variables

Create a file called `.env` in the root of the project with the following content:

```env
BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

| Variable         | Description           | Where to get it                                                      |
| ---------------- | --------------------- | -------------------------------------------------------------------- |
| `BOT_TOKEN`      | Telegram bot token    | Talk to [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` |
| `GEMINI_API_KEY` | Google Gemini API key | [aistudio.google.com](https://aistudio.google.com) → Get API Key     |

> ⚠️ Never share or commit your `.env` file. It is already listed in `.gitignore`.

---

## Managing the Knowledge Base

The bot's knowledge comes entirely from the files in the `knowledge_base/` folder. No code changes needed — just manage the files.

| Action                  | How                                   |
| ----------------------- | ------------------------------------- |
| **Add a topic**         | Drop a new PDF into `knowledge_base/` |
| **Update a topic**      | Replace the PDF with a new version    |
| **Remove a topic**      | Delete the PDF from the folder        |
| **Temporarily disable** | Move the file outside the folder      |

The bot reloads the files automatically every 50 messages, so **no restart is needed** after editing.

### Supported file formats

| Format | How to create                                    |
| ------ | ------------------------------------------------ |
| `.pdf` | Export from Word, Google Docs, LibreOffice, etc. |
| `.txt` | Any plain text editor                            |

---

## Telegram Commands

| Command   | Description                                           |
| --------- | ----------------------------------------------------- |
| `/start`  | Welcome message with topic list                       |
| `/status` | Shows which knowledge base files are currently loaded |

---

## .gitignore

Make sure your `.gitignore` includes at minimum:

```
.env
venv/
__pycache__/
*.pyc
```

---

## Dependencies

| Package               | Purpose                      |
| --------------------- | ---------------------------- |
| `python-telegram-bot` | Telegram Bot API wrapper     |
| `python-dotenv`       | Loads `.env` variables       |
| `google-genai`        | Google Gemini AI API         |
| `pdfplumber`          | Extracts text from PDF files |
