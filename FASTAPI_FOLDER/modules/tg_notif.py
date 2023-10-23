import os
import time

import requests

# chat_id = "403278079"


def check_and_notify(name, chat_id):
    # Замените следующие значения на ваш Telegram bot token и chat_id
    bot_token = "6413423789:AAElRZhIcR-iQaY_6jsUx3Mag-MtyIpCQzw"
    notification_sent = False

    filepath = os.path.join("/RUNFILES", f"{name}.txt")
    while True:
        with open(filepath, "r") as f:
            content = f.read()
            if "Synthesis complete" in content and not notification_sent:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {"chat_id": chat_id, "text": "Synthesis complete"}
                requests.post(url, payload)
                print("Telegram notification sent.")
                notification_sent = (
                    True  # Установите флаг, чтобы не отправлять уведомление снова
                )
                break  # Выход из цикла
            else:
                print("Synthesis not complete yet. Checking again in 2 minutes.")

                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": "Synthesis not complete yet. Checking again in 2 minutes.",
                }
                requests.post(url, payload)
                print("Telegram notification sent.")
                notification_sent = (
                    False  # Установите флаг, чтобы не отправлять уведомление снова
                )

                time.sleep(120)  # Пауза на 2 минуты
