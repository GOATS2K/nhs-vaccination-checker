import requests
from nhs_vaccination_checker import config

PUSHBULLET_API = "https://api.pushbullet.com/v2"


def notify_user(date) -> dict:
    body = {
        "type": "note",
        "title": "NHS Vaccination Checker",
        "body": f"Early appointment found at {date}",
    }
    r = requests.post(
        f"{PUSHBULLET_API}/pushes",
        headers={"Access-Token": config.get("DEFAULT", "pushbullet_token")},
        json=body,
    )
    return r.json()


def test_notification() -> dict:
    body = {
        "type": "note",
        "title": "NHS Vaccination Checker",
        "body": "Notification system works!",
    }
    r = requests.post(
        f"{PUSHBULLET_API}/pushes",
        headers={"Access-Token": config.get("DEFAULT", "pushbullet_token")},
        json=body,
    )
    return r.json()
