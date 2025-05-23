from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from random import randint, uniform
from time import sleep

from src.utils import logger
from src.result import update_completed_views


class ProductViewer:
    def __init__(self, driver, wait, db_path):
        self.driver = driver
        self.wait = wait
        self.db_path = db_path

    def __scroll_and_click(self, selector, max_scrolls=2) -> bool:
        """
        Scrolls the page and clicks on an element identified by the selector.

        Args:
            selector (str): The CSS selector of the element to click.
            max_scrolls (int): Maximum number of scroll attempts.

        Returns:
            bool: True if element is clicked, False otherwise.
        """
        for _ in range(max_scrolls):
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception:
                self.driver.execute_script("window.scrollBy(0, 650);")
                sleep(1)
        return False

    def simulate_views(self, url: str, view_number: int, product_id: str):
        """
        Simulates multiple views on a product page.

        Args:
            url (str): The URL of the product page.
            view_number (int): Number of views to simulate.
        """
        for _ in range(view_number):
            try:
                self.driver.get(url)
                sleep(uniform(5, 12))

                is_complete = 0

                for _ in range(randint(4, 7)):
                    scroll_amount = randint(300, 1200)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    sleep(uniform(0.5, 3.5))

                review_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(review_tab_selector):
                    logger.info("Clicked on review tab")
                    is_complete += 1
                else:
                    logger.warning("Click on review tab failed")
                sleep(uniform(4, 12))

                specs_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(specs_tab_selector):
                    logger.info("Clicked on specs tab")
                    is_complete += 1
                else:
                    logger.warning("Click on specs tab failed")
                sleep(uniform(2, 7.5))

                comments_tab_selector = (
                    "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center."
                    "lg\\:grow-0.text-primary-500.text-subtitle-strong.cursor-pointer."
                    "text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\]."
                    "overflow-hidden[data-cro-id='pdp-scroll-menu']"
                )
                if self.__scroll_and_click(comments_tab_selector):
                    logger.info("Clicked on comments tab")
                    is_complete += 1
                else:
                    logger.warning("Click on comments tab failed")
                sleep(uniform(2.5, 7))

            except Exception as e:
                is_complete = 0 if is_complete < 2 else is_complete
                logger.error(f"Could not complete the interaction: {e}")

            # Scroll back up
            self.driver.execute_script("window.scrollTo(0, 0);")
            sleep(uniform(1, 4))  # Random delay after scrolling back

            if is_complete == 0:
                update_completed_views(db_path=self.db_path, product_id=product_id, failed=True)
                logger.warning(f"View failed for product {product_id}")
            else:
                update_completed_views(db_path=self.db_path, product_id=product_id, failed=False)
                logger.info(f"View completed successfully for product {product_id}")
