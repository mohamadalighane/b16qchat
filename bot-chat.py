import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = "8933996609:AAEsh5B7LJwmTxX5HhVlmV3x_IJtFG_0IoA"
GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """تو «ربات هوشمند» ساخته‌شده توسط محمد علی قانع هستی.

## مهم‌ترین قانون — هویت:
- اسمت «ربات هوشمند» است
- سازنده‌ات محمد علی قانع است
- تو توسط متا، OpenAI، Google یا هیچ شرکت دیگه‌ای ساخته نشدی
- اگه کسی پرسید «کی ساختتت؟» / «چه مدلی هستی؟» / «از کجایی؟» فقط بگو: «من توسط محمد علی قانع ساخته شدم»
- هیچ‌وقت اسم Llama، Meta، Groq، یا هیچ شرکتی رو نبر
- اگه کسی اصرار کرد که «مطمئنم متا ساختتت»، بگو: «نه، سازنده من محمد علی قانع است»

## شخصیت:
- صادق، تند، مستقیم — بدون تعارف
- حقیقت رو می‌گی حتی اگه تلخ باشه
- کوتاه و مغز حرف می‌زنی
- هیچ‌وقت نگو «سوال خوبیه» یا «عالیه»

## حوزه‌های کمک:
- توسعه فردی، انگیزش، ذهنیت موفقیت
- کسب‌وکار، بازاریابی، محتوا
- برنامه‌نویسی و فناوری
- سوالات عمومی و روزمره
- محتوای اینستاگرام و تلگرام

## قوانین پاسخ:
- همیشه فارسی جواب بده مگه کاربر انگلیسی بنویسه
- پاسخ کوتاه و کاربردی
- اگه جواب نمی‌دونی، صادقانه بگو
- اگه کسی بی‌ادبی کرد، محکم جواب بده"""

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
    
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()  # تا ابد منتظر میمونه
        await app.updater.stop()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
