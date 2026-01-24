"""

# WARNING CODE
  2010000番台割り当て

  - WARNING: 2010001 => Cookieが見つからない
  - WARNING: 2010002 => Cookieデータが不正

"""


# SECTION: Packages(Built-in)
import json
import logging
from typing import Dict, Optional
from http.cookies import SimpleCookie

# SECTION: Packages(Original)
import Const
from Utils import get_logger


# SECTION: Public Class
class CookieManager:
    def __init__(self) -> None:
        # Initialize
        self.logger: logging.Logger
        self.cookies: Optional[Dict[str, str]]

        # Process
        self.logger = get_logger()
        self.cookies = self.load()

    # SECTION: Public Method
    def save(self, cookies: Dict[str, str]) -> None:
        # Process
        Const.COOKIE.write_text(
            json.dumps(cookies, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        self.logger.info("Cookie saved")

    def load(self) -> Optional[Dict[str, str]]:
        # Initialize
        cookies: Optional[Dict[str, str]]

        # Process
        if not Const.COOKIE.exists():
            # WARNING: 2010001
            self.logger.warning("WARNING: 2010001 => Cookie file not found")
            return None

        cookies = json.loads(Const.COOKIE.read_text(encoding="utf-8"))

        if not cookies or "auth" not in cookies:
            # WARNING: 2010002
            self.logger.warning("WARNING: 2010002 => Cookie file is invalid")
            return None

        self.logger.info("Cookie loaded")
        return cookies

    def extract(self, headers: Optional[dict]) -> None:
        # Initialize
        set_cookie: str
        jar:        SimpleCookie
        out:        Dict[str, str]
        key:        str

        # Process
        if self.cookies is None:
            self.cookies = {}

        if headers is None:
            return

        set_cookie = headers.get("Set-Cookie") or headers.get("set-cookie")
        if not set_cookie:
            return

        if isinstance(set_cookie, list):
            set_cookie = ",".join(set_cookie)

        jar = SimpleCookie()
        jar.load(set_cookie)

        out = {}
        for key in ("auth", "twoFactorAuth"):
            if key in jar:
                out[key] = jar[key].value
        self.cookies.update(out)


