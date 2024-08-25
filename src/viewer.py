from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint, uniform
from time import sleep

from src.utils import logger


def scroll_and_click(driver, wait, selector, max_scrolls=5):
    """
    Scrolls the page and clicks on an element identified by the selector.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        selector (str): The CSS selector of the element to click.
        max_scrolls (int): Maximum number of scroll attempts.

    Returns:
        bool: True if element is clicked, False otherwise.
    """
    for scroll in range(max_scrolls):
        try:
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            logger.warning(f"Scrolling and clicking failed in try {scroll + 1}")
            driver.execute_script("window.scrollBy(0, 400);")
            sleep(1)
    return False


def viewer(driver, wait, url: str, view_number: int):
    """
    Simulates multiple views on a product page.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        url (str): The URL of the product page.
        view_number (int): Number of views to simulate.
    """
    for i in range(view_number):
        driver.get(url)
        sleep(uniform(2, 5))

        for _ in range(randint(4, 7)):
            scroll_amount = randint(200, 1100)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            sleep(uniform(0.5, 1.5))

        try:
            review_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
            if scroll_and_click(driver, wait, review_tab_selector):
                logger.info("Clicked on First button")
            sleep(uniform(2, 6))

            specs_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
            if scroll_and_click(driver, wait, specs_tab_selector):
                logger.info("Clicked on Second button")
            sleep(uniform(1, 3))

            comments_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-primary-500.text-subtitle-strong.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
            if scroll_and_click(driver, wait, comments_tab_selector):
                logger.info("Clicked on Third button")
            sleep(uniform(2, 5))

            see_all_comments_selector = "span.inline-flex.items-center.cursor-pointer.styles_Anchor--secondary__3KsgY.text-button-2.my-auto"
            if scroll_and_click(driver, wait, see_all_comments_selector):
                logger.info("Clicked on Last button")
            sleep(uniform(4, 7))

        except Exception as e:
            logger.error(f"Could not complete the interaction: {e}")

        # Scroll back up
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(uniform(1, 3))  # Random delay after scrolling back

        logger.info(f"View {i+1} completed")
