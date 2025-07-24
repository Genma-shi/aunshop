from firebase_admin import messaging

def send_fcm_notification(title, body, fcm_token, sound="default", data=None):
    """
    Отправка push-уведомления с кастомным звуком и кроссплатформенной поддержкой.
    """
    try:
        message = messaging.Message(
            token=fcm_token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data={k: str(v) for k, v in (data or {}).items()},
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound=sound
                    )
                )
            ),
            android=messaging.AndroidConfig(
                notification=messaging.AndroidNotification(
                    sound=sound
                )
            )
        )
        response = messaging.send(message)
        print(f"[FCM] Уведомление отправлено: {response}")
    except Exception as e:
        print(f"[FCM] Ошибка отправки: {e}")
