import uuid
from datetime import datetime

from rasa_sdk import Tracker

from common import send_console_request


def send_notification(tracker: Tracker, event: dict):
    """Send a notification using the notifications-gateway"""
    return send_console_request(
        "notifications", "/notifications", tracker, "post", json=event
    )


def send_rbac_request_admin(
    tracker: Tracker,
    org_id: str,
    username: str,
    requested_url: str,
    user_email: str,
    user_message: str,
):
    event = dict(
        {
            "id": uuid.uuid4(),
            "bundle": "console",
            "application": "rbac",
            "event_type": "request-access",
            "timestamp": datetime.now().isoformat(),
            "org_id": org_id,
            "context": {},
            "events": [
                {
                    "metadata": {},
                    "payload": {
                        "url_path": requested_url,
                        "username": username,
                        "user": {"email": user_email, "request": user_message},
                    },
                }
            ],
            "recipients": [{"only_admins": True}],
        }
    )

    return send_notification(tracker, event)