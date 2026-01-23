"""

# ERROR CODE
  1010000番台割り当て

  - ERROR: 1010001 => イベントの登録に失敗

"""


# SECTION: Packages(Built-in)
import os
import time
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

# SECTION: Packages(Third-party)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# SECTION: Packages(Original)
from . import Controller
from Data import Payload
from Utils import get_logger


# SECTION: Class
class FormsRequest:
    def __init__(self, timeout: int = 10, test: bool = False) -> None:
        # Initialize
        self.logger: logging.Logger
        self.timeout: int
        self.driver: webdriver.Chrome
        self.wait: WebDriverWait
        self.sequencer: List[Dict[str, callable]]
        self.test: bool
        self.interval: int
        self.last_exec: Optional[datetime]

        # Process
        self.logger = get_logger()
        self.timeout = timeout
        self.driver = self.__create_driver()
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.sequencer = self.__sequencer()
        self.test = test
        self.interval = 3
        self.last_exec = None

        if self.test:
            self.sequencer.pop(-1)

    # SECTION: Public Methods
    def close(self) -> None:
        self.driver.close()

    def quit(self) -> None:
        self.driver.quit()

    def submit(self, payload: Payload) -> None:
        # Initialize
        ctx: Controller.FormsContext
        obj: Dict[str, str]

        # Process
        if payload.lock_exist_forms:
            self.logger.info(f"{payload.section}:{payload.event_name} はすでに登録されています")
            return

        if self.last_exec is not None:
            self.__wait_process()

        self.logger.info(f"{payload.section}:{payload.event_name} の処理を開始")

        self.logger.info("VRChatイベントカレンダー登録処理開始")
        try:
            self.logger.info(f"Load URL: {payload.forms_url}")
            self.driver.get(payload.forms_url)
            self.logger.info("ページ読み込み処理完了")

            # UI操作
            for sequence in self.sequencer:
                ctx = Controller.FormsContext(payload, self.driver, self.wait, sequence["element"])
                sequence["controller"](ctx)
                self.logger.info(f"{sequence["name"]}終了")

        except Exception as e:
            # ERROR: 1010001
            self.logger.error(e)
            self.logger.error(f"ERROR: 1010001 => {payload.event_name} の登録処理に失敗しました")
        else:
            self.logger.info("VRChatイベントカレンダー登録終了")

            os.makedirs(f"tracer/{payload.section}", exist_ok=True)

            obj = self.__obj_template(payload)

            try:
                with open(payload.lock_target_forms, "w", encoding="utf-8") as f:
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
    def __create_driver(self) -> webdriver.Chrome:
        # Initialize
        options: Options
        service: Service

        # Process
        self.logger.info("ChromeDriver initialize start")

        options = Options()
        options.add_experimental_option(
            "debuggerAddress",
            f"127.0.0.1:9222",
        )
        service = Service(ChromeDriverManager().install())

        self.logger.info("ChromeDriver initialize end")

        return webdriver.Chrome(service=service, options=options)

    def __wait_process(self) -> None:
        # Initialize
        now: datetime

        # Process
        now = datetime.now()

        if (now - self.last_exec).seconds < self.interval:
            self.logger.info("処理インターバル待ち")

        while (now - self.last_exec).seconds < self.interval:
            now = datetime.now()

    # SECTION: Template
    @staticmethod
    def __obj_template(payload: Payload) -> Dict[str, str]:
        # Process
        return {
            **payload.payload_identity,
            "registered_at": datetime.now().isoformat(timespec="seconds")
        }

    @staticmethod
    def __sequencer() -> List[Dict[str, callable]]:
        # Process
        return [
            # フォームの上書き確認ボタンをクリック
            {
                "name": "上書き確認ボタン処理",
                "controller": Controller.click_overwrite,
                "element": "//div[@role='alertdialog']//a[.//span[text()='続行']]"
            },
            # 返信用メールアドレスのチェックボックスをクリック
            {
                "name": "返信用アドレスチェック処理",
                "controller": Controller.click_checkbox,
                "element": "//div[@role='checkbox' and contains(@aria-label,'返信に表示するメールアドレスとして')]"
            },
            # イベント詳細情報登録画面に遷移
            {
                "name": "イベント詳細ページへの遷移処理",
                "controller": Controller.click_button,
                "element": "//div[@role='button' and (.//span[text()='次へ'] or .//span[text()='Next'])]"
            },
            # イベント主催者入力
            {
                "name": "イベント主催者入力処理",
                "controller": Controller.input_text_owner,
                "element": "//div[@role='heading' and .//span[contains(text(),'イベント主催者')]]"
            },
            # イベント内容入力
            {
                "name": "イベント内容入力処理",
                "controller": Controller.input_text_desc,
                "element": "//textarea[contains(@aria-labelledby,'i6')]"
            },
            # イベントカテゴリー選択
            {
                "name": "イベントカテゴリー選択処理",
                "controller": Controller.select_category_checkbox,
                "element": "//div[@role='checkbox' and @aria-label='{}']"
            },
            # 参加条件の記入
            {
                "name": "イベント参加条件の記入処理",
                "controller": Controller.input_text_condition,
                "element": "//div[@role='heading' and .//span[contains(text(),'参加条件')]]"
            },
            # 参加方法の記入
            {
                "name": "イベント参加方法の記入処理",
                "controller": Controller.input_text_direction,
                "element": "//div[@role='heading' and .//span[contains(text(),'参加方法')]]"
            },
            # 備考の記入
            {
                "name": "イベント備考の記入処理",
                "controller": Controller.input_text_remarks,
                "element": "//div[@role='heading' and .//span[contains(text(),'備考')]]"
            },
            # 送信ボタンをクリック
            {
                "name": "イベント登録リクエスト処理",
                "controller": Controller.click_button_submit,
                "element": "//div[@role='button' and (.//span[text()='送信'] or .//span[text()='Submit'])]"
            }
        ]
