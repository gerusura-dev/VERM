import os
import json
from pathlib import Path
from logging import Logger
from typing import Optional, Dict, Any

import vrchatapi


COOKIE_PATH = Path.home() / ".vrc_cookies.json"


class CookieManager:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.cookie: Optional[Dict[str, Any]] = None
        self.load()

    def __call__(self) -> Optional[dict]:
        return self.cookie

    def load(self) -> Optional[dict]:
        if self.cookie is None:
            self.__load_cookie()
        return self.cookie

    def save(self, api_client: vrchatapi.ApiClient) -> None:
        self.__save_cookie(api_client)

    @property
    def enable(self) -> bool:
        return bool(self.cookie and self.cookie.get("authCookie"))

    def __load_cookie(self) -> None:
        if not COOKIE_PATH.exists():
            self.logger.warning("Cookieファイルが見つかりません: %s", COOKIE_PATH)
            self.cookie = None
            return

        try:
            data = json.loads(COOKIE_PATH.read_text(encoding="utf-8"))

            # 旧形式/破損/空を弾く
            auth = data.get("authCookie")
            twofa = data.get("twoFactorAuthCookie")
            if not auth:
                self.logger.warning("Cookieファイルはあるが authCookie が空です: %s", COOKIE_PATH)
                self.cookie = None
                return

            self.cookie = {
                "authCookie": auth,
                "twoFactorAuthCookie": twofa,
            }
        except Exception as e:
            self.logger.exception("Cookieファイルの読み込みに失敗: %s", e)
            self.cookie = None

    def __save_cookie(self, api_client: vrchatapi.ApiClient) -> None:
        """
        http.cookiejar.CookieJar 互換で auth / twoFactorAuth を取り出して保存する
        """
        try:
            jar = api_client.rest_client.cookie_jar

            def pick(name: str) -> Optional[str]:
                # http.cookiejar.CookieJar は .get() がないのでイテレートして探す
                for c in jar:
                    try:
                        if c.name == name:
                            return c.value
                    except Exception:
                        continue
                return None

            auth_cookie = pick("auth")
            twofa_cookie = pick("twoFactorAuth")

            if not auth_cookie:
                self.logger.error(
                    "auth cookie が取得できませんでした（get_current_user() 成功後に save() を呼んでいるか確認）"
                )
                return

            data = {
                "authCookie": auth_cookie,
                "twoFactorAuthCookie": twofa_cookie,
            }

            COOKIE_PATH.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            try:
                os.chmod(COOKIE_PATH, 0o600)
            except Exception as e:
                self.logger.warning("chmodに失敗: %s", e)

            self.cookie = data
            self.logger.info("Cookieを保存しました: %s", COOKIE_PATH)

        except Exception as e:
            self.logger.exception("Cookie保存に失敗: %s", e)