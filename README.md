import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me your AliExpress link and I will clean it for Bluesky.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if "aliexpress" not in text.lower():
        await update.message.reply_text("Please send an AliExpress link.")
        return
    # Remove tracking junk after ?
    clean = text.split("?")[0]
    reply = f"Check this out 🔥\n\n{clean}\n\n#AliExpress #Deals"
    await update.message.reply_text(reply)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.run_polling()

