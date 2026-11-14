# 🎨 Telegram AI Image Generator & Gemini Assistant Bot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/likker0123/telegram-ai-image-bot)

यह एक आधुनिक Telegram बोट है जो **AI Image Generation** और **Google Gemini 2.5 Flash** दोनों को सपोर्ट करता है। इसे सीधे **Render** पर एक क्लिक में फ्री वेब सर्विस के रूप में डिप्लॉय किया जा सकता है।

---

## 🌟 फीचर्स
- **AI Image Generation:** किसी भी प्रॉम्प्ट (`/image <प्रॉम्प्ट>` या सीधा टेक्स्ट) से HD इमेज जनरेट करता है।
- **Google Gemini Chat:** बोट से कोई भी सवाल पूछें, Gemini 2.5 Flash द्वारा तुरंत उत्तर पाएँ।
- **1-Click Render Deploy:** `render.yaml` ब्लूप्रिंट से Render पर सीधा डिप्लॉय।
- **Auto Webhook:** Render पर अपने-आप Webhook मोड और लोकल पर Polling मोड स्विच करता है।

---

## 🚀 Render पर लाइव करने का तरीका
1. ऊपर दिए गए **Deploy to Render** बटन पर क्लिक करें (या [इस लिंक](https://render.com/deploy?repo=https://github.com/likker0123/telegram-ai-image-bot) को खोलें)।
2. Render आपसे दो एनवायरनमेंट वेरिएबल्स मांगेगा:
   - `BOT_TOKEN`: आपका Telegram Bot Token
   - `GEMINI_API_KEY`: आपका Gemini API Key
3. **Apply** दबाएँ—आपका बोट Render पर 24/7 लाइव हो जाएगा!

---

## 💻 लोकल टेस्टिंग (Local Run)
```bash
git clone https://github.com/likker0123/telegram-ai-image-bot.git
cd telegram-ai-image-bot
pip install -r requirements.txt
python bot.py
```
