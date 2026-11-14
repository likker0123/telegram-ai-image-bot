# 🎨 Telegram AI Image Generator Bot (Render Ready)

यह एक आधुनिक Telegram AI इमेज जनरेटर बोट है जिसे Python में तैयार किया गया है और यह **Render** पर फ्री वेब सर्विस के रूप में चलने के लिए पूरी तरह तैयार है।

---

## 🌟 फीचर्स
- **AI Image Generation:** किसी भी प्रॉम्प्ट (`/image <प्रॉम्प्ट>` या सीधा टेक्स्ट) से HD इमेज जनरेट करता है।
- **कोई अतिरिक्त API Key नहीं:** इमेज जेनरेशन तुरंत फ्री में काम करता है।
- **Render Ready:** Render पर ऑटो-वेबहुक (Webhook) और लोकल पर Polling दोनों मोड अपने-आप डिटेक्ट करता है।

---

## 📁 फ़ाइलें
- [bot.py](file:///C:/Users/ayush/.gemini/antigravity/scratch/telegram-bot/bot.py) – मुख्य AI इमेज जनरेटर बोट कोड
- [requirements.txt](file:///C:/Users/ayush/.gemini/antigravity/scratch/telegram-bot/requirements.txt) – आवश्यक Python लाइब्रेरी
- [render.yaml](file:///C:/Users/ayush/.gemini/antigravity/scratch/telegram-bot/render.yaml) – Render डिप्लॉयमेंट कॉन्फ़िगरेशन
- [.env.example](file:///C:/Users/ayush/.gemini/antigravity/scratch/telegram-bot/.env.example) – एनवायरनमेंट वेरिएबल्स प्रारूप

---

## 🚀 1. Telegram Bot Token प्राप्त करें
1. Telegram ऐप पर `@BotFather` खोजें।
2. `/newbot` भेजकर अपने बोट का नाम और यूज़रनेम सेट करें।
3. BotFather से प्राप्त **API Token** कॉपी करें।

---

## 💻 2. लोकल टेस्टिंग
```bash
cd C:\Users\ayush\.gemini\antigravity\scratch\telegram-bot
pip install -r requirements.txt
set BOT_TOKEN="आपका_BOT_TOKEN"
python bot.py
```
Telegram पर अपने बोट को `/image cute puppy playing in snow` भेजकर टेस्ट करें!

---

## 🌐 3. Render पर लाइव करने के चरण
1. इस फ़ोल्डर को अपने **GitHub Repository** में पुश करें।
2. [dashboard.render.com](https://dashboard.render.com/) पर लॉगिन करें।
3. **New + > Web Service** पर क्लिक करें और अपनी GitHub रिपॉजिटरी चुनें।
4. सेटिंग्स:
   - **Name:** `telegram-image-bot`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** `Free`
5. **Environment Variables** में जोड़ें:
   - Key: `BOT_TOKEN`
   - Value: `<आपका Telegram Bot Token>`
6. **Deploy Web Service** पर क्लिक करें। Render पर बोट लाइव हो जाएगा!
