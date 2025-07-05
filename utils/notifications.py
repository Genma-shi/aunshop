# utils/notifications.py
from firebase_admin import messaging

def send_fcm_notification(title, body, fcm_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token,
    )
    response = messaging.send(message)
    print("✅ Уведомление отправлено:", response)
