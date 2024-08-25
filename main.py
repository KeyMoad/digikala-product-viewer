from argparse import ArgumentParser
from selenium.webdriver.support.ui import WebDriverWait
from sys import exit
import chromedriver_autoinstaller

from settings import BASE_PRODUCT_URL, DEFAULT_TIMEOUT, PROXY_LIST_URLS, ID_LIST_FILE, PROXY_TYPE
from src.utils import logger, read_product_ids
from src.viewer import ProductViewer
from src.driver import DriverManager
from src.proxy import ProxyManager


def main(view_number: int, product_ids: list):
    """
    Main function to initiate viewing process for each product.

    Args:
        view_number (int): Number of views to simulate.
        product_ids (list): List of product IDs.
    """
    proxy_manager = ProxyManager(PROXY_LIST_URLS)
    driver_manager = DriverManager(proxy_manager, PROXY_TYPE)

    for product_id in product_ids:
        url = f'{BASE_PRODUCT_URL}/{product_id.strip()}'
        logger.info(f'Starting view process for product {product_id.strip()} [{url}] ...')

        driver = driver_manager.get_driver()
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        viewer = ProductViewer(driver, wait)
        
        viewer.simulate_views(url, view_number)
        
        driver.quit()


if __name__ == '__main__':
    # Setup argument parser
    parser = ArgumentParser(description='Simulate product views on a digikala.')
    parser.add_argument('view_number', type=int, help='Number of views to simulate for each product.')

    # Parse arguments
    args = parser.parse_args()

    # Read product IDs from the ID_LIST_FILE
    product_ids = read_product_ids(ID_LIST_FILE)
    
    # Check if product_ids is not empty
    if not product_ids:
        logger.error(f'No product IDs found in {ID_LIST_FILE} the list. Exiting...')
        exit(1)

    # Automatically install the correct version of chromedriver
    chromedriver_autoinstaller.install()

    try:
        main(args.view_number, product_ids)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
