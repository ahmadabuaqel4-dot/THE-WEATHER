import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# --- (هذا الجزء الخدعة لكي يرضى موقع Render ولا يغلق البوت) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

t = threading.Thread(target=run_server)
t.start()
# -------------------------------------------------------------

# التوكين الخاص بك (استبدله إذا غيرته)
TELEGRAM_TOKEN = "9253097178:AAHaYPsuirhXZ5nAR1kjvPDtX95-MPHDHVU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك في بوت الطقس! 🌤️\n"
        "أرسل لي اسم أي مدينة (بالإنجليزي) لأعطيك حالة الطقس فوراً."
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
        await update.message.reply_text(reply_message, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("عذراً، لم أستطع العثور على هذه المدينة. تأكد من كتابة الاسم بالإنجليزية.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    print("البوت يعمل الآن...")
    app.run_polling()