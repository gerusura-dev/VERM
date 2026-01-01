import time
import json
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from .builder import Payload


class AutoSubmitter:
    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.driver = self._create_driver()

    @staticmethod
    def _create_driver() -> webdriver.Chrome:
        options = Options()

        options.add_experimental_option(
            "debuggerAddress",
            f"127.0.0.1:9222",
        )

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def submit(self, payload: Payload) -> None:
        try:
            driver = self.driver
            driver.get(payload.url)

            wait = WebDriverWait(driver, self.timeout)

            # 入力内容の履歴を無視して上書きする
            time.sleep(0.3)
            overwrite_element = "//div[@role='alertdialog']//a[.//span[text()='続行']]"
            self.__click_overwrite(driver, wait, overwrite_element)

            # 返信用メールアドレスをチェックする
            time.sleep(0.3)
            checkbox_element = "//div[@role='checkbox' and contains(@aria-label,'返信に表示するメールアドレスとして')]"
            self.__click_checkbox(driver, wait, checkbox_element)

            # 次へボタンをクリック
            time.sleep(1)
            next_button_element = "//div[@role='button' and (.//span[text()='次へ'] or .//span[text()='Next'])]"
            self.__click_button(wait, next_button_element)

            # イベント主催者を記入する
            time.sleep(0.3)
            self.__owner_input_text(driver, wait, payload.owner)

            # イベント内容を記入する
            time.sleep(0.3)
            description_element = "//textarea[contains(@aria-labelledby,'i6')]"
            self.__input_text(wait, description_element, payload.desc)

            # イベントのカテゴリーをチェックする
            time.sleep(0.3)
            if payload.category is not None:
                self.__select_category_checkbox(driver, wait, payload.category.value)

            # 参加条件を記入
            time.sleep(0.3)
            condition_element = "参加条件"
            self.__input_text_by_heading(driver, wait, condition_element, payload.condition)

            # 参加方法を記入
            time.sleep(0.3)
            direction_element = "参加方法"
            self.__input_text_by_heading(driver, wait, direction_element, payload.direction)

            # 備考を記入
            time.sleep(0.3)
            remarks_element = "備考"
            self.__input_text_by_heading(driver, wait, remarks_element, payload.remarks)

            # 送信ボタンをクリック
            time.sleep(1)
            self.__click_submit_button(driver, wait)
        except:
            raise RuntimeError
        else:
            with open(f"tracer/{payload.section}/{payload.hash}.json", "w", encoding="utf-8") as f:
                json.dump(
                    {
                        **payload.payload_identity(),
                        "registered_at": datetime.now().isoformat(timespec="seconds")
                    },
                    f,
                    ensure_ascii=False,
                    indent=2
                )

            time.sleep(3)


    def close(self) -> None:
        self.driver.close()

    @staticmethod
    def __click_overwrite(driver: webdriver.Chrome, wait: WebDriverWait, element: str) -> None:
        try:
            link = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        element
                    )
                )
            )

            driver.execute_script("arguments[0].click();", link)

        except TimeoutException:
            pass

    @staticmethod
    def __click_checkbox(driver: webdriver.Chrome, wait: WebDriverWait, element: str) -> None:
        checkbox = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    element
                )
            )
        )

        if checkbox.get_attribute("aria-checked") != "true":
            driver.execute_script("arguments[0].click();", checkbox)

    @staticmethod
    def __click_button(wait: WebDriverWait, element: str) -> None:
        button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    element
                )
            )
        )

        button.click()


    @staticmethod
    def __owner_input_text(driver: webdriver.Chrome, wait: WebDriverWait, value: str) -> None:
        heading = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@role='heading' and .//span[contains(text(),'イベント主催者')]]"
                )
            )
        )

        container = heading.find_element(
            By.XPATH,
            "ancestor::div[contains(@jsmodel,'CP1oW')]"
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", container
        )
        driver.execute_script("arguments[0].click();", container)

        input_box = container.find_element(By.XPATH, ".//input[@type='text']")

        input_box.send_keys(value)

        driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            input_box,
        )

    @staticmethod
    def __input_text(wait: WebDriverWait, element: str, value: str) -> None:
        input_box = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    element
                )
            )
        )

        input_box.send_keys(value)

    @staticmethod
    def __select_category_checkbox(driver: webdriver.Chrome, wait: WebDriverWait, label_text: str) -> None:
        checkbox = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@role='checkbox' and @aria-label='{label_text}']"
                )
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        if checkbox.get_attribute("aria-checked") != "true":
            driver.execute_script(
                "arguments[0].click();",
                checkbox
            )

    @staticmethod
    def __input_text_by_heading(driver: webdriver.Chrome, wait: WebDriverWait, heading_text: str, value: str) -> None:
        heading = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@role='heading' and .//span[contains(text(),'{heading_text}')]]"
                )
            )
        )

        container = heading.find_element(
            By.XPATH,
            "ancestor::div[contains(@jsmodel,'CP1oW')]"
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", container
        )
        driver.execute_script("arguments[0].click();", container)

        textarea = container.find_element(By.XPATH, ".//textarea")

        textarea.clear()
        textarea.send_keys(value)

        driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            textarea,
        )

    @staticmethod
    def __click_submit_button(driver: webdriver.Chrome, wait: WebDriverWait) -> None:
        submit_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@role='button' and (.//span[text()='送信'] or .//span[text()='Submit'])]"
                )
            )
        )

        driver.execute_script("arguments[0].click();", submit_button)
