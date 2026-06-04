import requests
import json
import time

# =========================
# CONFIGURATION
# =========================

BOT_TOKEN = "8817474328:AAGv7lV_6qO-kOgJIsUy2Tw_rCSKgb2FEK4"
API_URL = "https://exploitsindia.site/anish/api.php?key=imlasahu&num=number"

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# =========================
# TELEGRAM FUNCTIONS
# =========================

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = f"{BASE_URL}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    if parse_mode:
        data["parse_mode"] = parse_mode

    try:
        requests.post(url, data=data, timeout=30)
    except Exception as e:
        print("Send message error:", e)


def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"

    params = {
        "timeout": 30
    }

    if offset:
        params["offset"] = offset

    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print("Get updates error:", e)
        return {"ok": False, "result": []}


# =========================
# EXTERNAL API
# =========================

def call_external_api(number):
    try:
        response = requests.get(
            API_URL,
            params={"number": number},
            timeout=30
        )

        return response.json()

    except Exception as e:
        return {
            "error": str(e)
        }


# =========================
# KEYBOARD
# =========================

def main_keyboard():
    return {
        "keyboard": [
            [
                {"text": "📱 Phone Lookup"}
            ]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


# =========================
# MAIN BOT LOOP
# =========================

offset = None

print("Bot started...")

while True:
    try:
        updates = get_updates(offset)

        if updates.get("ok"):
            for update in updates.get("result", []):

                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message["chat"]["id"]

                text = message.get("text", "").strip()

                # /start command
                if text == "/start":
                    send_message(
                        chat_id,
                        "Welcome! Choose an option below.",
                        reply_markup=main_keyboard()
                    )
                    continue

                # Phone Lookup button
                if text == "📱 Phone Lookup":
                    send_message(
                        chat_id,
                        "Send 10 digit mobile number:"
                    )
                    continue

                # Validate number
                if text.isdigit():

                    if len(text) != 10:
                        send_message(
                            chat_id,
                            "❌ Invalid number. Please send exactly 10 digits."
                        )
                        continue

                    api_result = call_external_api(text)

                    formatted = json.dumps(
                        api_result,
                        indent=4,
                        ensure_ascii=False
                    )

                    send_message(
                        chat_id,
                        f"<pre>{formatted}</pre>",
                        parse_mode="HTML"
                    )

                    continue

                send_message(
                    chat_id,
                    "❌ Invalid input. Use /start and select Phone Lookup."
                )

        time.sleep(1)

    except Exception as e:
        print("Main loop error:", e)
        time.sleep(5)
