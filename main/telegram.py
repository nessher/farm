from http.client import responses
import requests
from django.conf import settings


def send_telegram_message(text: str, chat_id: str | int | None = None) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN:
        print('Telegram token не задан в settings')
        return False

    chat_id = chat_id or settings.TELEGRAM_ADMIN_CHAT_ID
    if not chat_id:
        print('CHAT_ID не задан')
        return False

    url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, json=payload, timeout=7)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f'Ошибка отправки в Telegram: {e}')
        return False