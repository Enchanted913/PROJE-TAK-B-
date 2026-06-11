import logging
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)
_firebase_app = None


def _get_firebase_app():
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app
    cred_path = settings.FIREBASE_CREDENTIALS
    if not cred_path or not Path(cred_path).exists():
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials

        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            _firebase_app = firebase_admin.initialize_app(cred)
        else:
            _firebase_app = firebase_admin.get_app()
        return _firebase_app
    except Exception as exc:
        logger.warning('Firebase başlatılamadı: %s', exc)
        return None


def send_push_notification(token: str, title: str, body: str) -> bool:
    if not token:
        return False
    app = _get_firebase_app()
    if not app:
        logger.info('FCM (simülasyon): %s - %s', title, body)
        return False
    try:
        from firebase_admin import messaging

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=token,
        )
        messaging.send(message)
        return True
    except Exception as exc:
        logger.warning('FCM gönderilemedi: %s', exc)
        return False
