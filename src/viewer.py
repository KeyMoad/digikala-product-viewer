from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint, uniform
from time import sleep
from src.utils import logger


class ProductViewer:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def __scroll_and_click(self, selector, max_scrolls=5) -> bool:
        """
        Scrolls the page and clicks on an element identified by the selector.

        Args:
            selector (str): The CSS selector of the element to click.
            max_scrolls (int): Maximum number of scroll attempts.

        Returns:
            bool: True if element is clicked, False otherwise.
        """
        for scroll in range(max_scrolls):
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception:
                logger.warning(f"Scroll attempt {scroll + 1} failed")
                self.driver.execute_script("window.scrollBy(0, 400);")
                sleep(1)
        return False

    def simulate_views(self, url: str, view_number: int):
        """
        Simulates multiple views on a product page.

        Args:
            url (str): The URL of the product page.
            view_number (int): Number of views to simulate.
        """
        for _ in range(view_number):
            self.driver.get(url)
            sleep(uniform(5, 12))

            for _ in range(randint(4, 7)):
                scroll_amount = randint(200, 1100)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                sleep(uniform(0.5, 3.5))

            try:
                review_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(review_tab_selector):
                    logger.info("Clicked on review tab")
                sleep(uniform(4, 12))

                specs_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(specs_tab_selector):
                    logger.info("Clicked on specs tab")
                sleep(uniform(2, 7.5))

                comments_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-primary-500.text-subtitle-strong.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(comments_tab_selector):
                    logger.info("Clicked on comments tab")
                sleep(uniform(2.5, 7))

                see_all_comments_selector = (
                    "span.inline-flex.items-center.cursor-pointer."
                    "styles_Anchor--secondary__3KsgY.text-button-2.my-auto"
                )
                if self.__scroll_and_click(see_all_comments_selector):
                    logger.info("Clicked on see all comments")
                sleep(uniform(4, 10))

            except Exception as e:
                logger.error(f"Could not complete the interaction: {e}")

            # Scroll back up
            self.driver.execute_script("window.scrollTo(0, 0);")
            sleep(uniform(1, 4))  # Random delay after scrolling back

            logger.info(f"View completed")
