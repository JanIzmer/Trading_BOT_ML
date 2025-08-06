import time
import requests
from config import TELEGRAM_CONFIG
from core.users import save_user

BOT_TOKEN = TELEGRAM_CONFIG['bot_token']
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

OFFSET = None

def get_updates():
    """
    Fetch new updates (messages) from the Telegram bot API.

    Returns:
        dict: JSON response containing updates.
    """
    global OFFSET
    url = f"{API_URL}/getUpdates"
    if OFFSET:
        url += f"?offset={OFFSET}"
    response = requests.get(url)
    return response.json()

def handle_updates(updates):
    """
    Process incoming updates, register users, and send a confirmation message.

    Args:
        updates (dict): JSON object with update data from Telegram.
    """
    global OFFSET
    for update in updates.get("result", []):
        OFFSET = update["update_id"] + 1
        try:
            chat = update["message"]["chat"]
            chat_id = chat["id"]
            save_user(chat_id)
            print(f"✅ User registered: {chat_id}")
            send_message(chat_id, "📩 You are registered to receive signals.")
        except Exception as e:
            print("❌ Error processing update:", e)

def send_message(chat_id, text):
    """
    Send a text message to a Telegram chat.

    Args:
        chat_id (int): Unique identifier for the target chat.
        text (str): Message text to send.
    """
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    print("🤖 Bot started...")
    while True:
        updates = get_updates()
        handle_updates(updates)
        time.sleep(2)
