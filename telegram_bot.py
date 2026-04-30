import os
from dotenv import load_dotenv
load_dotenv()
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.environ.get("8736434524:AAFM9KbwzLOZWQrr3qCsWLQ2KBLquCm0sTs")

if not BOT_TOKEN:
if not BOT_TOKEN:
    print("⚠️ BOT_TOKEN missing")
print("✅ TOKEN LOADED")

LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]
user_state = {}

# =========================
# SAMPLE FUNCTIONS
# =========================
def sales_location(location):
    return f"📊 {location} SALES\n💰 ₹1,25,000\n🧾 Orders: 320\n📦 AOV: ₹390"

def staff_location(location):
    return f"📍 {location} STAFF\nTop: KRISHNA\nLow: RAMESH"

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📊 Sales", "👨‍🍳 Captain"]]
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
        await update.message.reply_text(sales_location(text))
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