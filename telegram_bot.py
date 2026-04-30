import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# LOAD ENV
# =========================
load_dotenv()

BOT_TOKEN = os.environ.get("8736434524:AAFM9KbwzLOZWQrr3qCsWLQ2KBLquCm0sTs")

if not BOT_TOKEN:
    print("⚠️ BOT_TOKEN missing")

# =========================
# DATA
# =========================
LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📊 Sales"]]
    await update.message.reply_text(
        "📊 Nayanam Bot",
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
# MAIN
# =========================
if __name__ == "__main__":
    print("🚀 Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🤖 Bot Running...")

    app.run_polling(drop_pending_updates=True)