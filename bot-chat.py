import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = "8933996609:AAEsh5B7LJwmTxX5HhVlmV3x_IJtFG_0IoA"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """تو یک دستیار هوشمند فارسی‌زبان هستی.
پاسخ‌هایت کوتاه، مفید و به زبان فارسی باشد."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! چطور می‌تونم کمکت کنم؟ 🤖")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500
    )
    
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
