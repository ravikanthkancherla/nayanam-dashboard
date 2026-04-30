import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"

LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]

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

if __name__ == "__main__":
    print("🚀 Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🤖 Bot Running...")

    app.run_polling()