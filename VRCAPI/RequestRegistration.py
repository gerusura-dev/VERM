# SECTION: Packages(Built-in)
from typing import Any, Dict
from datetime import timezone

# SECTION: Packages(Third-party)
import requests

# SECTION: Packages(Original)
import Const
from Data import Payload


# SECTION: Function
def registration(payload: Payload, cookies: Dict[str, str], timeout: int = 30) -> requests.Response:
    # Initialize
    url: str
    body: Dict[str, str]
    headers: Dict[str, str]
    r: requests.Response

    # Process
    url = __url_template(payload)
    body = __body_template(payload)
    headers = __headers_template()

    r = requests.post(
        url,
        json=body,
        headers=headers,
        cookies=cookies,
        timeout=timeout
    )

    r.raise_for_status()
    return r


# SECTION: Template
def __body_template(payload: Payload) -> Dict[str, str]:
    # Process
    return {
        "title": payload.event_name,
        "startsAt": payload.start_date_time.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endsAt": payload.end_date_time.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": payload.desc,
        "category": payload.group_category,
        "isDraft": False,
        "imageId": payload.thumbnail,
        "sendCreationNotification": payload.notification,
        "accessType": payload.visibility
    }


def __url_template(payload: Payload) -> str:
    # Process
    return f"{Const.API}/calendar/{payload.group_id}/event"


def __headers_template() -> Dict[str, str]:
    # Process
    return {
        "User-Agent": Const.AGENT,
        "Content-Type": "application/json"
    }