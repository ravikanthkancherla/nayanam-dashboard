import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

from bot import load_data, sales_location, staff_location
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")

ALLOWED_USERS = {
    8583468705: "admin",
    807377060: "user"
}

user_state = {}

def main_menu():
    return ReplyKeyboardMarkup(
        [["📊 Sales", "👨‍💼 Captain"],
         ["👤 Employee Details"]],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Not authorized")
        return

    await update.message.reply_text("📊 Nayanam Bot", reply_markup=main_menu())

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    msg = update.message.text.strip()

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Not authorized")
        return

    df = load_data()

    if msg == "📊 Sales":
        user_state[user_id] = {"type": "sales"}

    elif msg == "👨‍💼 Captain":
        user_state[user_id] = {"type": "captain"}

    elif msg == "👤 Employee Details":
        await update.message.reply_text("👤 Module coming soon")
        return

    if msg in ["📊 Sales", "👨‍💼 Captain"]:

        outlets = df["Outlet"].dropna().unique().tolist()
        keyboard = [[o] for o in outlets]

        await update.message.reply_text(
            "📍 Select Location",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if user_id in user_state and "location" not in user_state[user_id]:
        user_state[user_id]["location"] = msg

        keyboard = [
            ["Today", "Yesterday"],
            ["📅 Custom Date"],
            ["📆 Month"]
        ]

        await update.message.reply_text(
            "📅 Select Date",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if msg == "📅 Custom Date":
        await update.message.reply_text("Enter DD-MM-YYYY")
        return

    if msg == "📆 Month":
        await update.message.reply_text("Enter MM-YYYY")
        return

    if user_id in user_state:

        state = user_state[user_id]
        outlet = state.get("location")

        if msg == "Today":
            date_mode = "today"
        elif msg == "Yesterday":
            date_mode = "yesterday"
        else:
            date_mode = msg

        if state["type"] == "sales":
            result = sales_location(df, outlet, date_mode)
        else:
            result = staff_location(df, outlet, date_mode)

        await update.message.reply_text(result, reply_markup=main_menu())

        user_state.pop(user_id, None)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🤖 Bot Running...")
app.run_polling()