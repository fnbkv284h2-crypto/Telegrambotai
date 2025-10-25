import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
last_update_id = 0

def get_updates():
    global last_update_id
    url = f"{BASE_URL}/getUpdates?timeout=10&offset={last_update_id + 1}"
    try:
        response = requests.get(url, timeout=20)
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print("⚠️ خطأ أثناء جلب التحديثات:", e)
        return []

def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage", data={"chat_id": chat_id, "text": text})
    except Exception as e:
        print("⚠️ خطأ أثناء إرسال الرسالة:", e)

def ask_openai(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
    }
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        j = r.json()
        return j["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("⚠️ خطأ أثناء الاتصال بـ OpenAI:", e)
        return "حدث خطأ أثناء الاتصال بالذكاء الاصطناعي 😔"

def main():
    global last_update_id
    print("🤖 البوت بدأ العمل...")

    while True:
        updates = get_updates()
        for update in updates:
            last_update_id = update["update_id"]
            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text.lower() in ["/start", "ابدأ", "مرحبا"]:
                send_message(chat_id, "أهلاً! أرسل لي أي سؤال وسأجيبك باستخدام الذكاء الاصطناعي 🤖")
                continue

            send_message(chat_id, "💭 جاري التفكير...")
            reply = ask_openai(text)
            send_message(chat_id, reply)

        time.sleep(2)

if __name__ == "__main__":
    main()