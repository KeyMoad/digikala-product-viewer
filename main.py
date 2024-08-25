from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

from settings import BASE_PRODUCT_URL, DEFAULT_TIMEOUT, PROXY_LIST_URLS
from src.utils import logger
from src.viewer import viewer
from src.driver import get_driver
from src.proxy import ProxyManager


def main(view_number: int, list_of_id: list):
    """
    Main function to initiate viewing process for each product.

    Args:
        view_number (int): Number of views to simulate.
        list_of_id (list): List of product IDs.
    """
    for product_id in list_of_id:
        url = PRODUCT_URL(product_id.strip())
        logger.info(f'Checking product {product_id.strip()} [{url}] ...')
        viewer(driver, wait, url, view_number)


if __name__ == '__main__':
    # Get product ID/s and number of views from user input
    product_ids = input('Enter product IDs separated by commas: ').strip().split(',')
    view_number = int(input('Enter the number of views: '))

    # Automatically install the correct version of chromedriver
    chromedriver_autoinstaller.install()

    proxy_manager = ProxyManager(PROXY_LIST_URLS)

    driver = get_driver(proxy=proxy_manager.get_random_proxy())

    # Wait for elements to be available (timeout after 10 seconds)
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # Final url lambda
    PRODUCT_URL = lambda product_id : f'{BASE_PRODUCT_URL}/{product_id}'

    # Run the main function
    try:
        main(view_number, product_ids)
    finally:
        driver.quit()
