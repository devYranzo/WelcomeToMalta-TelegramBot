"""
main.py — Malta Bot with Knowledge Base (RAG)
----------------------------------------------
Flujo simplificado:
  1. Usuario manda un mensaje
  2. Gemini responde usando SOLO el knowledge base como contexto
  3. Si la pregunta no está en el KB, lo dice claramente

Para controlar qué sabe el bot → edita los archivos de /knowledge_base/
"""

import os
import re
from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
from context_loader import load_knowledge_base, get_loaded_topics

# ------------------ CONFIG ------------------
load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN") or ""
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY") or ""

client = genai.Client(api_key=GEMINI_API_KEY)

KNOWLEDGE_BASE: str = load_knowledge_base()
MESSAGE_COUNT: int = 0
REFRESH_EVERY: int = 50  # Recarga el KB cada 50 mensajes sin reiniciar


# ------------------ HELPERS ------------------

def md_to_html(text: str) -> str:
    """Convierte Markdown a HTML por si Gemini no hace caso."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text


def maybe_refresh_kb() -> None:
    global KNOWLEDGE_BASE, MESSAGE_COUNT
    MESSAGE_COUNT += 1
    if MESSAGE_COUNT % REFRESH_EVERY == 0:
        KNOWLEDGE_BASE = load_knowledge_base()


# ------------------ AI RESPONSE ------------------

def get_ai_response(user_text: str) -> str:
    """Llama a Gemini con el knowledge base como único contexto."""
    try:
        system_prompt = f"""You are a helpful assistant for newcomers and expats living in Malta.

            CRITICAL RULES:
            1. Answer ONLY using the information in the KNOWLEDGE BASE below. Do not use outside knowledge.
            2. If the question is not covered, say exactly: "I don't have specific info on that yet. Feel free to ask about housing, transport, health, or general life in Malta! 🇲🇹"
            3. Use ONLY HTML tags for formatting: <b>bold</b>, <i>italic</i>. NEVER use Markdown (**bold**, *italic*).
            4. Be friendly, concise, and practical.
            5. Include relevant links from the knowledge base when available (plain URLs, Telegram renders them).
            6. End with a short friendly closing like "Feel free to ask anything else! 🇲🇹"

            --- KNOWLEDGE BASE ---
            {KNOWLEDGE_BASE}
            --- END ---
            """
        prompt = f"{system_prompt}\n\nUser: {user_text}"
        response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
        raw = response.text or "I'm not sure about that. Try asking about housing, transport, or health in Malta!"
        return md_to_html(raw)

    except Exception as e:
        print(f"[AI Error] {e}")
        return "⚠️ Something went wrong. Please try again in a moment."


# ------------------ HANDLERS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "👋 <b>Welcome to Malta!</b> 🇲🇹\n\n"
        "I can help you with:\n"
        "🏠 <b>Housing</b> — rooms, rent, areas\n"
        "🚍 <b>Transport</b> — buses, Bolt, ferries\n"
        "📱 <b>SIM cards</b> — providers, data plans\n"
        "🛒 <b>Shopping</b> — supermarkets, delivery\n"
        "🏥 <b>Health</b> — hospitals, pharmacies\n"
        "🎉 <b>Nightlife</b> — Paceville, clubs\n"
        "🌅 <b>Places</b> — beaches, sightseeing\n\n"
        "Just type your question! 💬",
        parse_mode="HTML"
    )


async def admin_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/status — muestra qué temas del KB están activos. Solo para admins."""
    if not update.effective_message:
        return

    topics = get_loaded_topics()
    if not topics:
        await update.effective_message.reply_text("⚠️ No knowledge base files found.")
        return

    lines = ["📚 <b>Knowledge Base Status</b>\n"]
    for topic, fmt in topics.items():
        icon = "📄" if fmt == "PDF" else "📝"
        lines.append(f"{icon} <b>{topic}</b> ({fmt})")

    lines.append(f"\n🔄 Auto-refresh every {REFRESH_EVERY} messages.")
    await update.effective_message.reply_text("\n".join(lines), parse_mode="HTML")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    maybe_refresh_kb()

    ai_text = get_ai_response(update.message.text)
    await update.message.reply_text(ai_text, parse_mode="HTML")


# ------------------ RUN ------------------

if __name__ == "__main__":
    print(f"[KB] Loaded {len(KNOWLEDGE_BASE)} chars of knowledge base context")
    print(f"[KB] Active topics: {[t for t, e in get_loaded_topics().items() if e]}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", admin_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()
