import json
import getpass
from pathlib import Path
from logging import Logger

from http.cookies import SimpleCookie
from typing import Dict, Tuple, Optional

import vrchatapi
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode


USER_AGENT = "VRCEventRegistrationManager/0.1.0 contact@verm.com"
COOKIE_PATH = Path.home() / ".vrc_cookies.json"


def login(logger: Logger) -> Dict[str, str]:
    cookies = load_vrc_cookies(logger)
    user = cookie_login(logger, cookies)

    if user is None:
        logger.info("cookie not found, login manually")

        username = input("username or email: ")
        password = getpass.getpass("password: ")

        user, cookies = manual_login(username, password)
        save_vrc_cookies(cookies)

    logger.info("login success: %s", user.presence.display_name)

    return cookies


def save_vrc_cookies(cookies: Dict[str, str]) -> None:
    COOKIE_PATH.write_text(
        json.dumps(cookies, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def load_vrc_cookies(logger: Logger) -> Dict[str, str] | None:
    if not COOKIE_PATH.exists():
        logger.warning("cookie file not found: %s", COOKIE_PATH)
        return None
    return json.loads(COOKIE_PATH.read_text(encoding="utf-8"))


def cookie_login(logger: Logger, cookies: Dict[str, str]) -> Optional[vrchatapi.models.current_user.CurrentUser]:
    if not cookies or "auth" not in cookies:
        logger.warning("cookie not found")
        return None

    client = make_client_with_cookies(
        auth=cookies["auth"],
        two_factor_auth=cookies.get("twoFactorAuth")
    )

    auth_api = authentication_api.AuthenticationApi(client)
    try:
        return auth_api.get_current_user()
    except Exception:
        return None


def manual_login(username: str, password: str) -> Tuple[vrchatapi.models.current_user.CurrentUser, Dict[str, str]]:
    configuration = vrchatapi.Configuration(
        username=username,
        password=password
    )

    cookies: Dict[str, str] = {}

    with make_client(configuration) as client:
        auth_api = authentication_api.AuthenticationApi(client)

        try:
            user, _, headers = auth_api.get_current_user_with_http_info()
            cookies.update(_extract_auth_cookies(headers))
            return user, cookies
        except UnauthorizedException as e:
            cookies.update(_extract_auth_cookies(getattr(e, "headers", None)))
            ensure_2fa_if_needed(auth_api, e)
            user, _, headers = auth_api.get_current_user_with_http_info()
            cookies.update(_extract_auth_cookies(headers))
            return user, cookies


def make_client(configuration: vrchatapi.Configuration) -> vrchatapi.ApiClient:
    api_client = vrchatapi.ApiClient(configuration)
    api_client.user_agent = USER_AGENT
    return api_client


def make_client_with_cookies(auth: str, two_factor_auth: Optional[str] = None) -> vrchatapi.ApiClient:
    configuration = vrchatapi.Configuration()

    api_client = vrchatapi.ApiClient(configuration)
    api_client.user_agent = USER_AGENT

    cookie_header = f"auth={auth}"
    if two_factor_auth:
        cookie_header += f"; twoFactorAuth={two_factor_auth}"

    api_client.default_headers["Cookie"] = cookie_header
    return api_client


def ensure_2fa_if_needed(auth_api: authentication_api.AuthenticationApi, e: UnauthorizedException) -> None:
    if getattr(e, "status", None) == 200:
        reason = getattr(e, "reason", "") or ""
        if "Email 2 Factor Authentication" in reason:
            code = input("Email 2FA Code: ").strip()
            auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(code))
        elif "2 Factor Authentication" in reason:
            code = input("2FA Code (Authenticator): ").strip()
            auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(code))


def _extract_auth_cookies(headers: Optional[dict]) -> Dict[str, str]:
    if not headers:
        return {}

    set_cookie = headers.get("Set-Cookie") or headers.get("set-cookie")
    if not set_cookie:
        return {}

    if isinstance(set_cookie, list):
        set_cookie = ",".join(set_cookie)

    jar = SimpleCookie()
    jar.load(set_cookie)

    out: Dict[str, str] = {}
    for key in ("auth", "twoFactorAuth"):
        if key in jar:
            out[key] = jar[key].value
    return out
