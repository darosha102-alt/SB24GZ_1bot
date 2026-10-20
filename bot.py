import io
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pyrxing import read_barcode
from PIL import Image

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am @SB24GZ_1bot.\n"
        "Send me an image containing a QR code or barcode, and I will try to scan the content."
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_bytes = await photo_file.download_as_bytearray()
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        barcode = read_barcode(image)
        
        if barcode is not None:
            reply = f"✅ Scan successful!\n\nContent: {barcode.text}\nFormat: {barcode.format}"
        else:
            reply = "❌ No QR code or barcode recognized. Please ensure the code is clear and complete."
    except Exception as e:
        logger.error(f"Scan error: {e}")
        reply = "⚠️ Error during scanning. Please try again with a clearer image."
    
    await update.message.reply_text(reply)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        return
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
