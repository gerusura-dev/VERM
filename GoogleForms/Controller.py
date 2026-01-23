# SECTION: Packages(Built-in)
from time import sleep
from typing import Iterable
from dataclasses import dataclass

# SECTION: Packages(Third-party)
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec

# SECTION: Packages(Original)
from Data import Payload


# SECTION: Common Class
@dataclass(frozen=True)
class FormsContext:
    payload: Payload
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str

    def __iter__(self) -> Iterable:
        return iter((self.payload, self.driver, self.wait, self.element))


# SECTION: Common Function
def __presence_element(wait: WebDriverWait,element: str) -> WebElement:
    # Process
    return wait.until(
        ec.presence_of_element_located(
            (
                By.XPATH,
                element
            )
        )
    )


def __get_container(wait: WebDriverWait, element: str) -> WebElement:
    # Initialize
    heading: WebElement

    # Process
    heading = __presence_element(wait, element)
    return heading.find_element(
        By.XPATH,
        "ancestor::div[contains(@jsmodel,'CP1oW')]"
    )


def __input_text_heading(ctx: FormsContext, value: str) -> None:
    # Initialize
    payload: Payload
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    container: WebElement
    textarea: WebElement

    # Process
    payload, driver, wait, element = ctx

    container = __get_container(wait, element)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        container
    )
    driver.execute_script(
        "arguments[0].click();",
        container
    )

    textarea = container.find_element(By.XPATH, ".//textarea")

    textarea.clear()
    textarea.send_keys(value)

    driver.execute_script(
        """
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """,
        textarea
    )


# SECTION: Function
def click_overwrite(ctx: FormsContext) -> None:
    # Initialize
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    link: WebElement

    # Process
    _, driver, wait, element = ctx

    try:
        link = __presence_element(wait, element)
        driver.execute_script(
            "arguments[0].click();",
            link
        )
    except TimeoutException:
        pass
    except Exception as e:
        print(e)


def click_checkbox(ctx: FormsContext) -> None:
    # Initialize
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    checkbox: WebElement

    # Process
    _, driver, wait, element = ctx

    checkbox = __presence_element(wait, element)
    if checkbox.get_attribute("aria-checked") != "true":
        driver.execute_script(
            "arguments[0].click();",
            checkbox
        )


def click_button(ctx: FormsContext) -> None:
    # Initialize
    wait: WebDriverWait
    element: str
    button: WebElement

    # Process
    _, _, wait, element = ctx

    button = __presence_element(wait, element)
    button.click()


def click_button_submit(ctx: FormsContext) -> None:
    # Initialize
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    button: WebElement

    # Process
    _, driver, wait, element = ctx

    button = __presence_element(wait, element)
    driver.execute_script(
        "arguments[0].click();",
        button
    )


def input_text_owner(ctx: FormsContext) -> None:
    # Initialize
    payload: Payload
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    heading: WebElement
    container: WebElement
    input_box: WebElement

    # Process
    payload, driver, wait, element = ctx

    container = __get_container(wait, element)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        container
    )

    driver.execute_script(
        "arguments[0].click();",
        container
    )

    input_box = container.find_element(By.XPATH, ".//input[@type='text']")
    input_box.send_keys(payload.owner)

    driver.execute_script(
        """
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """,
        input_box
    )


def input_text_desc(ctx: FormsContext) -> None:
    # Initialize
    payload: Payload
    wait: WebDriverWait
    element: str
    input_box: WebElement

    # Process
    payload, _, wait, element = ctx

    input_box = __presence_element(wait, element)
    input_box.send_keys(payload.desc)


def input_text_condition(ctx: FormsContext) -> None:
    # Process
    __input_text_heading(ctx, ctx.payload.condition)


def input_text_direction(ctx: FormsContext) -> None:
    # Process
    __input_text_heading(ctx, ctx.payload.direction)


def input_text_remarks(ctx: FormsContext) -> None:
    # Process
    __input_text_heading(ctx, ctx.payload.remarks)


def select_category_checkbox(ctx: FormsContext) -> None:
    # Initialize
    payload: Payload
    driver: webdriver.Chrome
    wait: WebDriverWait
    element: str
    checkbox: WebElement

    # Process
    payload, driver, wait, element = ctx

    for category in payload.event_category:
        checkbox = __presence_element(wait, element.format(category))

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            checkbox
        )

        if checkbox.get_attribute("aria-checked") != "true":
            driver.execute_script(
                "arguments[0].click();",
                checkbox
            )
