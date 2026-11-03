import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ⚠️ هام جداً: استبدل النص التالي بالتوكين (Token) الحقيقي الخاص بك الذي أخذته من BotFather
TELEGRAM_TOKEN = "9253097178:AAHAyPSuirhXZ5nAR1kjvPDtX95-MPHDHVU"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك في بوت الطقس! 🌤️\n"
        "أرسل لي اسم أي مدينة بالإنجليزية (مثلاً: Amman) لأعطيك حالة الطقس فوراً."
    )


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url).json()
        current_condition = response["current_condition"][0]

        temp_c = current_condition["temp_C"]
        feels_like = current_condition["FeelsLikeC"]
        humidity = current_condition["humidity"]
        weather_desc = current_condition["weatherDesc"][0]["value"]

        reply_message = (
            f"🌍 **حالة الطقس في {city.capitalize()}:**\n\n"
            f"🌡️ درجة الحرارة: {temp_c}°C\n"
            f"🤔 الشعور الفعلي: {feels_like}°C\n"
            f"💧 الرطوبة: {humidity}%\n"
            f"☁️ الحالة: {weather_desc}"
        )
        await update.message.reply_text(
            reply_message, parse_mode="Markdown"
        )
    except Exception:
        await update.message.reply_text(
            "عذراً، لم أستطع العثور على هذه المدينة. تأكد من كتابة الاسم باللغة الإنجليزية بشكل صحيح."
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather)
    )

    print("✅ البوت يعمل الآن... اذهب لتليجرام وجربه!")
    app.run_polling()