import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get(HTTP API:8608867667:AAHjLC8fJSQjKuavUiALVDwYKXS-BKiqJG8)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me an AliExpress link and I will help you with it."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "aliexpress" in text.lower():
        await update.message.reply_text(f"Got your link: {text}\nI am working on it...")
    else:
        await update.message.reply_text("Please send me an AliExpress link.")

def main():
    app = ApplicationBuilder().token(HTTP API:8608867667:AAHJjLC8fJSQjKuavUiALVDwYKXS-BKiqJG8).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
