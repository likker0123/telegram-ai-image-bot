import os
import logging
import urllib.parse
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PORT = int(os.getenv("PORT", "8080"))
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"नमस्ते {user_name}! 🎨🤖\n\n"
        "मैं आपका **AI Image & Gemini Assistant Bot** हूँ!\n\n"
        "✨ **इमेज जनरेट करने के लिए:**\n"
        "`/image a futuristic cybernetic tiger in neon jungle`\n\n"
        "💬 **बातचीत करने के लिए:**\n"
        "मुझे कोई भी सवाल या मैसेज भेजें, मैं Google Gemini द्वारा उत्तर दूँगा।\n\n"
        "सहायता के लिए /help दबाएँ।"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 **उपलब्ध फीचर्स:**\n\n"
        "1. `/image <प्रॉम्प्ट>` या `/generate <प्रॉम्प्ट>` - AI द्वारा फोटो जनरेट करें।\n"
        "2. सामान्य चैट - Google Gemini से कोई भी सवाल पूछें, कोडिंग कराएँ या सलाह लें।\n"
        "3. `/start` - बोट रीस्टार्ट करें।"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def generate_image(update: Update, prompt: str):
    status_msg = await update.message.reply_text("⏳ आपकी इमेज बनाई जा रही है, कृपया 5-10 सेकंड प्रतीक्षा करें...")
    
    encoded_prompt = urllib.parse.quote(prompt.strip())
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=45)) as resp:
                if resp.status == 200:
                    image_bytes = await resp.read()
                    await update.message.reply_photo(
                        photo=image_bytes,
                        caption=f"✨ **प्रॉम्प्ट:** {prompt}\n🤖 Generated with AI"
                    )
                    await status_msg.delete()
                else:
                    await status_msg.edit_text("❌ इमेज जनरेट करने में समस्या आई। कृपया पुनः प्रयास करें।")
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await status_msg.edit_text("⚠️ टाइमआउट या नेटवर्क एरर। कृपया दोबारा प्रयास करें।")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ कृपया कोई प्रॉम्प्ट दें!\nउदाहरण: `/image cute baby elephant playing in water`", parse_mode="Markdown")
        return
    prompt = " ".join(context.args)
    await generate_image(update, prompt)

async def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API Key कॉन्फ़िगर नहीं है।"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        return candidates[0]["content"]["parts"][0]["text"]
                    return "क्षमा करें, उत्तर प्राप्त नहीं हुआ।"
                else:
                    err_text = await resp.text()
                    logger.error(f"Gemini API error ({resp.status}): {err_text}")
                    return "⚠️ Gemini API से संपर्क नहीं हो सका।"
    except Exception as e:
        logger.error(f"Gemini request exception: {e}")
        return "⚠️ नेटवर्क या टाइमआउट त्रुटि।"

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # If the user explicitly asks for an image in Hindi or English
    lower_text = text.lower()
    if lower_text.startswith("photo") or lower_text.startswith("image") or lower_text.startswith("तस्वीर") or lower_text.startswith("फोटो"):
        # Strip keyword
        cleaned = text.split(maxsplit=1)[-1] if len(text.split()) > 1 else text
        await generate_image(update, cleaned)
        return

    # Otherwise respond using Gemini
    await update.message.chat.send_action("typing")
    reply = await ask_gemini(text)
    await update.message.reply_text(reply)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", image_command))
    application.add_handler(CommandHandler("generate", image_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}/webhook"
        logger.info(f"Starting Webhook on port {PORT}: {webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=webhook_url,
        )
    else:
        logger.info("Starting Polling mode...")
        application.run_polling()

if __name__ == "__main__":
    main()
