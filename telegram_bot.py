import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.environ.get("8736434524:AAEytenE5d4MG2Fvh-b7PsV_3xPmlhKx_U4")

LOCATIONS = ["KOTHAPET", "BEGUMPET", "ASRAO", "ABIDS", "EAT STREET"]
user_state = {}

# =========================
# SAMPLE FUNCTIONS
# =========================
def sales_location(location, date="Today"):
    return f"""📊 {location} SALES

📅 Date: {date}
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

# =========================
# HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Sales", "👨‍🍳 Captain"],
        ["🔙 Menu"]
    ]

    await update.message.reply_text(
        "📊 Nayanam Intelligence Bot\nSelect an option:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # =========================
    # MAIN MENU
    # =========================
    if text == "📊 Sales":
        user_state[user_id] = "sales"

        keyboard = [[loc] for loc in LOCATIONS]
        keyboard.append(["🔙 Menu"])

        await update.message.reply_text(
            "Select Location:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif text == "👨‍🍳 Captain":
        user_state[user_id] = "staff"

        keyboard = [[loc] for loc in LOCATIONS]
        keyboard.append(["🔙 Menu"])

        await update.message.reply_text(
            "Select Location:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif text == "🔙 Menu":
        await start(update, context)
        return

    # =========================
    # SALES FLOW
    # =========================
    if user_state.get(user_id) == "sales" and text in LOCATIONS:
        result = sales_location(text)
        await update.message.reply_text(result)
        return

    # =========================
    # STAFF FLOW
    # =========================
    if user_state.get(user_id) == "staff" and text in LOCATIONS:
        result = staff_location(text)
        await update.message.reply_text(result)
        return


# =========================
# MAIN (FINAL STABLE)
# =========================
if __name__ == "__main__":
    print("🚀 Starting bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("🤖 Bot Running...")

    app.run_polling(
        poll_interval=2,
        timeout=30,
        bootstrap_retries=-1,
        drop_pending_updates=True
    )