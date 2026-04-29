import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ==============================
# CONFIG
# ==============================

BOT_TOKEN = os.environ.get("BOT_TOKEN")

LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]

user_state = {}

# ==============================
# DUMMY FUNCTIONS (REPLACE WITH YOUR LOGIC)
# ==============================

def sales_location(location, date="today"):
    return f"""📊 {location} SALES

Date: {date}

💰 Total Sales: ₹1,25,000
🧾 Orders: 320
📦 AOV: ₹390

📌 Sub Order Type:
Dine-In: 60%
Delivery: 30%
Takeaway: 10%
"""

def staff_location(location):
    return f"""📍 {location} STAFF PERFORMANCE

🏆 Top Performers:
KRISHNA → ₹1,20,000
ROHIT → ₹82,000

⚠️ Low Performers:
RAMESH → ₹29,000
PRAKASH → ₹18,000
"""

# ==============================
# HANDLERS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Sales", "👨‍🍳 Captain"],
        ["📦 Purchase Info", "📈 P&L"],
        ["👤 Employee Details"]
    ]

    await update.message.reply_text(
        "📊 *Nayanam Intelligence Bot*\nSelect an option:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # MAIN MENU
    if text == "📊 Sales":
        user_state[user_id] = "sales_location"

        keyboard = [[loc] for loc in LOCATIONS]
        keyboard.append(["🔙 Back"])

        await update.message.reply_text(
            "Select Location:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif text == "👨‍🍳 Captain":
        user_state[user_id] = "staff_location"

        keyboard = [[loc] for loc in LOCATIONS]
        keyboard.append(["🔙 Back"])

        await update.message.reply_text(
            "Select Location:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif text == "📦 Purchase Info":
        await update.message.reply_text(
            "🚧 Purchase Intelligence Engine is being fine-tuned.\nStay tuned for powerful insights!"
        )
        return

    elif text == "📈 P&L":
        await update.message.reply_text(
            "📊 Financial Engine warming up...\nP&L dashboards coming soon!"
        )
        return

    elif text == "👤 Employee Details":
        await update.message.reply_text(
            "👤 Employee intelligence system under development 🚧"
        )
        return

    elif text == "🔙 Back":
        await start(update, context)
        return

    # SALES FLOW
    if user_state.get(user_id) == "sales_location" and text in LOCATIONS:
        user_state[user_id] = ("sales_date", text)

        keyboard = [["Today", "Yesterday"], ["Custom Date"], ["🔙 Back"]]

        await update.message.reply_text(
            "Select Date:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif isinstance(user_state.get(user_id), tuple) and user_state[user_id][0] == "sales_date":
        location = user_state[user_id][1]

        if text == "Today":
            result = sales_location(location, "Today")
        elif text == "Yesterday":
            result = sales_location(location, "Yesterday")
        elif text == "Custom Date":
            user_state[user_id] = ("custom_date", location)
            await update.message.reply_text("Enter date (DD-MM-YYYY):")
            return
        else:
            result = "Invalid selection"

        await update.message.reply_text(result)
        await start(update, context)
        return

    elif isinstance(user_state.get(user_id), tuple) and user_state[user_id][0] == "custom_date":
        location = user_state[user_id][1]
        result = sales_location(location, text)

        await update.message.reply_text(result)
        await start(update, context)
        return

    # STAFF FLOW
    if user_state.get(user_id) == "staff_location" and text in LOCATIONS:
        result = staff_location(text)
        await update.message.reply_text(result)
        await start(update, context)
        return


# ==============================
# MAIN (ASYNC FIX FOR PYTHON 3.14)
# ==============================

async def main():
    print("🚀 Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🤖 Bot Running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())