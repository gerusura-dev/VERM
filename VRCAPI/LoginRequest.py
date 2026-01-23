"""

# WARNING CODE
  2020000番台割り当て

  - WARNING: 2020001 => ログイン失敗(Cookie)
  - WARNING: 2020002 => ログイン失敗(Manual)

"""


# SECTION: Packages(Built-in)
import json
import logging
import getpass
from datetime import datetime
from typing import Dict, Tuple, Optional

# SECTION: Packages(Third-party)
import requests
import vrchatapi
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.api.authentication_api import AuthenticationApi
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode

# SECTION: Packages(Original)
import Const
from Data import Payload
from Utils import get_logger
from .CookieManager import CookieManager
from .RequestRegistration import registration


# SECTION: Class
class LoginRequest:
    def __init__(self, test: bool = False) -> None:
        # Initialize
        self.logger: logging.Logger
        self.cookie_manager: CookieManager
        self.interval: int
        self.last_exec: Optional[datetime]
        self.test: bool

        # Process
        self.logger = get_logger()
        self.cookie_manager = CookieManager()
        self.interval = 60
        self.last_exec = None
        self.test = test

        self.login()

    # SECTION: Property
    @property
    def cookies(self) -> Dict[str, str]:
        # Process
        return self.cookie_manager.cookies

    @property
    def client(self) -> Tuple[bool, vrchatapi.ApiClient]:
        # Process
        if self.cookie_manager.cookies is None:
            return True, self.__make_client_manual()
        else:
            return False, self.__make_client_cookies(
                auth=self.cookie_manager.cookies["auth"],
                two_factor_auth=self.cookie_manager.cookies.get("twoFactorAuth")
            )

    # SECTION: Public Methods
    def login(self) -> None:
        # Initialize
        is_manual: bool
        client: vrchatapi.ApiClient
        auth: AuthenticationApi

        # Process
        is_manual, client = self.client
        auth = AuthenticationApi(client)

        if is_manual:
            self.__manual_login_request(auth)
        else:
            self.__cookie_login_request(auth)

    def submit(self, payload: Payload) -> None:
        # Initialize
        r: requests.Response
        obj: dict[str, str]

        # Process
        if self.test:
            return

        if payload.lock_exist_vrc_api:
            self.logger.info(f"{payload.section}:{payload.event_name} はすでに登録されています")
            return

        if self.last_exec is not None:
            self.__wait_process()

        r = registration(payload, self.cookies)
        self.logger.info(f"Status Code: {r.status_code}")

        obj = self.__obj_template(payload)

        try:
            with open(payload.lock_target_vrc_api, "w", encoding="utf-8") as f:
                json.dump(
                    obj,
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception as e:
            self.logger.error(e)
        else:
            self.logger.info("イベント登録履歴ファイル出力完了")

        self.last_exec = datetime.now()

    # SECTION: Private Methods
    def __wait_process(self) -> None:
        # Initialize
        now: datetime

        # Process
        now = datetime.now()

        if (now - self.last_exec).seconds < self.interval:
            self.logger.info("処理インターバル待ち")

        while (now - self.last_exec).seconds < self.interval:
            now = datetime.now()

    def __cookie_login_request(self, auth: AuthenticationApi) -> None:
        # Initialize
        try:
            _ = auth.get_current_user()
        except UnauthorizedException as e:
            # WARNING: 2020001
            self.logger.warning(e)
            self.logger.warning("WARNING: 2020001 => ログイン失敗(Cookie)")

            self.logger.info("Login retry with manual")
            self.__manual_login_request(auth)

    def __manual_login_request(self, auth: AuthenticationApi) -> None:
        # Initialize
        headers: Dict[str, str]

        # Process
        try:
            _, _, headers = auth.get_current_user_with_http_info()
            self.cookie_manager.extract(headers)
        except UnauthorizedException as e:
            # WARNING: 2020002
            self.logger.warning(e)
            self.logger.warning("WARNING: 2020002 => ログイン失敗(Manual)")

            self.logger.info("Login retry with ensure 2fa")
            self.cookie_manager.extract(getattr(e, "headers", None))
            self.__ensure_2fa_if_needed(auth, e)
            _, _, headers = auth.get_current_user_with_http_info()
            self.cookie_manager.extract(headers)

        self.cookie_manager.save(self.cookie_manager.cookies)

    @staticmethod
    def __make_client_manual() -> vrchatapi.ApiClient:
        # Initialize
        username: str
        password: str
        configuration: vrchatapi.Configuration
        api_client: vrchatapi.ApiClient

        # Process
        username = input("Username or Email: ")
        password = getpass.getpass("Password: ")

        configuration = vrchatapi.Configuration(
            username=username,
            password=password
        )

        api_client = vrchatapi.ApiClient(configuration)
        api_client.user_agent = Const.AGENT
        return api_client

    @staticmethod
    def __make_client_cookies(auth: str, two_factor_auth: Optional[str] = None) -> vrchatapi.ApiClient:
        # Initialize
        configuration: vrchatapi.Configuration
        api_client: vrchatapi.ApiClient
        cookie_header: str

        # Process
        configuration = vrchatapi.Configuration()

        api_client = vrchatapi.ApiClient(configuration)
        api_client.user_agent = Const.AGENT

        cookie_header = f"auth={auth}"
        if two_factor_auth:
            cookie_header += f"; twoFactorAuth={two_factor_auth}"

        api_client.default_headers["Cookie"] = cookie_header
        return api_client

    @staticmethod
    def __ensure_2fa_if_needed(auth: AuthenticationApi, e: UnauthorizedException) -> None:
        # Process
        if getattr(e, "status", None) == 200:
            reason = getattr(e, "reason", "") or ""
            if "Email 2 Factor Authentication" in reason:
                code = input("Email 2FA Code: ").strip()
                auth.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(code))
            elif "2 Factor Authentication" in reason:
                code = input("2FA Code (Authenticator): ").strip()
                auth.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(code))

    # SECTION: Template
    @staticmethod
    def __obj_template(payload: Payload) -> Dict[str, str]:
        # Process
        return {
            **payload.payload_identity,
            "registered_at": datetime.now().isoformat(timespec="seconds")
        }
