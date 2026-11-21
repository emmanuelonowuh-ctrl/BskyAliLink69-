import os, requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ALIEXPRESS_APP_KEY = os.environ.get("ALIEXPRESS_APP_KEY", "")
ALIEXPRESS_TRACKING_ID = os.environ.get("ALIEXPRESS_TRACKING_ID", "YOUR_TRACKING_ID")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")

# --- Helper: Make commission link ---
def make_affiliate_link(url):
    if ALIEXPRESS_TRACKING_ID and ALIEXPRESS_TRACKING_ID != "YOUR_TRACKING_ID":
        # AliExpress Portals format
        return f"https://s.click.aliexpress.com/e/_{ALIEXPRESS_TRACKING_ID}?url={url}"
    return url

# --- Helper: Search AliExpress (via API or fallback) ---
def search_aliexpress(query):
    # If you have API keys, this calls real API. Otherwise returns search link.
    # Real API endpoint: https://api-sg.aliexpress.com/sync
    # For now we use public search to get viral products
    search_url = f"https://www.aliexpress.com/wholesale?SearchText={query.replace(' ', '+')}"
    return search_url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! I find viral AliExpress products for your channel.\n\n"
        "Commands:\n"
        "/search <product> - Search product\n"
        "/viral - New viral products\n"
        "/trending - Trending today\n"
        "Just send me a photo name or send a product photo to save it!"
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Type: /search wireless earbuds")
        return
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching AliExpress for: {query}...")

    # Example products - replace with real API call when you add keys
    # This is the structure your API will fill
    products = [
        {"title": f"{query} - Viral 2026 Version", "price": "$4.99", "orig": "$12.99", "orders": "10k+ sold", "img": "https://picsum.photos/500", "url": search_aliexpress(query)},
        {"title": f"{query} - Pro Wireless", "price": "$7.49", "orig": "$19.99", "orders": "5k+ sold", "img": "https://picsum.photos/501", "url": search_aliexpress(query)},
        {"title": f"{query} - Mini Portable", "price": "$3.29", "orig": "$9.99", "orders": "8k+ sold", "img": "https://picsum.photos/502", "url": search_aliexpress(query)},
    ]

    for p in products:
        link = make_affiliate_link(p["url"])
        caption = (
            f"🔥 **{p['title']}**\n\n"
            f"💰 Price: {p['price']} (was {p['orig']})\n"
            f"📦 {p['orders']}\n\n"
            f"🔗 Buy here: {link}\n"
            f"#AliExpress #Viral"
        )
        try:
            await update.message.reply_photo(photo=p["img"], caption=caption, parse_mode="Markdown")
            # Save picture locally
            r = requests.get(p["img"])
            open(f"saved_{p['title'][:20]}.jpg", "wb").write(r.content)
        except:
            await update.message.reply_text(caption, parse_mode="Markdown")

async def viral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Fetching NEW viral products...")
    # Viral keywords that sell on Telegram
    for kw in ["mini projector", "led strip lights", "wireless earbuds"]:
        context.args = [kw]
        await search(update, context)

async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Trending Today on AliExpress:\n1. Car vacuum\n2. Portable blender\n3. Smart watch\n4. LED projector\n5. Hair straightener\n\nType /search <name> to get price + link")

async def chat_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # If user sends photo, save it
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        await file.download_to_drive(f"saved_{file.file_id}.jpg")
        await update.message.reply_text("✅ Picture saved! Send /search to find similar product.")
        return
    # Simple AI reply
    await update.message.reply_text(f"Got it: '{text}'\nType /search {text} to find it on AliExpress with price + commission link.")

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        await file.download_to_drive(f"saved_{file.file_id}.jpg")
        await update.message.reply_text("✅ Picture saved!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("viral", viral))
    app.add_handler(CommandHandler("trending", trending))
    app.add_handler(MessageHandler(filters.PHOTO, save_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_reply))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()