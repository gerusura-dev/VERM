from typing import Final
from pathlib import Path


"""
システムを利用する上で必要な定数を定義する

AGENT ... VRChatAPIに投げるリクエストに添付するUser-Agent
COOKIE ... ログイン認証用のCookieを保存しているPath
FORMS ... VRChatEventCalendarに使われているGoogleFormsのURL
API ... VRChatAPIのエンドポイント
"""


AGENT: Final[str] = "VERM/0.1.0 agent@verm.com"
COOKIE: Final[Path] = Path.home() / ".vrc_cookies.json"
FORMS: Final[str] = "https://docs.google.com/forms/d/e/1FAIpQLSfJlabb7niRTf4rX2Q0wRc3ua9MuOEIKveo7NirR6zuOo6D9A/viewform?usp=pp_url"
API: Final[str] = "https://api.vrchat.cloud/api/1"
