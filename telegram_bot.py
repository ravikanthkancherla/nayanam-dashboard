import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_URL")  # e.g. https://nayanam-telegram-bot.onrender.com

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing")
if not RENDER_URL:
    raise ValueError("RENDER_URL missing")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📊 Sales"]]
    await update.message.reply_text(
        "📊 Nayanam Bot\nSelect option:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 Sales":
        keyboard = [[loc] for loc in LOCATIONS]
        await update.message.reply_text(
            "Select Location:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if text in LOCATIONS:
        await update.message.reply_text(f"Sales for {text}: ₹1,25,000")
        return

# =========================
# MAIN (WEBHOOK MODE)
# =========================
if __name__ == "__main__":
    print("🚀 Starting webhook bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print(f"🔗 Setting webhook: {WEBHOOK_URL}")
    app.bot.set_webhook(WEBHOOK_URL)

    print("🤖 Bot Running...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL,
    )