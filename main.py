from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

from settings import BASE_PRODUCT_URL, DEFAULT_TIMEOUT, ID_LIST_FILE, HTTP_PROXY_LIST_URLS, SOCKS4_PROXY_LIST_URLS, SOCKS5_PROXY_LIST_URLS
from src.utils import logger, read_product_ids
from src.viewer import ProductViewer
from src.driver import DriverManager
from src.proxy import ProxyManager


def view_single_instance(product_id: str, proxy_manager: ProxyManager):
    """
    View a single instance of a product using a random proxy.
    
    Args:
        product_id (str): The product ID to view.
        proxy_manager (ProxyManager): Instance of ProxyManager to get proxies.
    """
    url = f'{BASE_PRODUCT_URL}/{product_id.strip()}'
    driver_manager = DriverManager(proxy_manager)
    driver = driver_manager.get_driver()
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    viewer = ProductViewer(driver, wait)
    viewer.simulate_views(url, 1)

    driver.quit()


def view_product_in_batches(product_id: str, view_number: int, batch_size: int, proxy_manager: ProxyManager):
    """
    Simulate views on a product in batches concurrently.
    
    Args:
        product_id (str): The product ID to view.
        view_number (int): The total number of views to simulate.
        batch_size (int): The number of concurrent views to run.
        proxy_manager (ProxyManager): Instance of ProxyManager to get proxies.
    """
    logger.info(f'Starting view process for product {product_id.strip()} with {view_number} views in batches of {batch_size}...')

    # Calculate the number of batches
    num_batches = (view_number + batch_size - 1) // batch_size

    for batch in range(num_batches):
        remaining_views = view_number - batch * batch_size
        current_batch_size = min(batch_size, remaining_views)
        logger.info(f'Running batch {batch + 1}/{num_batches} with {current_batch_size} views...')

        with ThreadPoolExecutor(max_workers=current_batch_size) as executor:
            futures = [
                executor.submit(view_single_instance, product_id, proxy_manager)
                for _ in range(current_batch_size)
            ]

            for future in as_completed(futures):
                try:
                    future.result()  # This will raise an exception if the callable raised one
                except Exception as e:
                    logger.error(f"An error occurred while processing a view: {e}")

    logger.info(f'Completed viewing process for product {product_id.strip()}')


def main(view_number: int, product_ids: list, batch_size: int, proxy_type: str, proxy_test_type: str):
    """
    Main function to initiate viewing process for each product in batches.

    Args:
        view_number (int): Number of views to simulate.
        product_ids (list): List of product IDs.
        batch_size (int): Number of concurrent views to run in each batch.
    """
    need_to_test = True if proxy_test_type else False

    if proxy_type == 'http':
        proxy_manager = ProxyManager(HTTP_PROXY_LIST_URLS, proxy_type, BASE_PRODUCT_URL, proxy_test_type, need_to_test)
    elif proxy_type == 'socks4':
        proxy_manager = ProxyManager(SOCKS4_PROXY_LIST_URLS, proxy_type, BASE_PRODUCT_URL, proxy_test_type, need_to_test)
    elif proxy_type == 'socks5':
        proxy_manager = ProxyManager(SOCKS5_PROXY_LIST_URLS, proxy_type, BASE_PRODUCT_URL, proxy_test_type, need_to_test)
    else:
        raise ValueError(f"Unsupported proxy type: {proxy_type}")

    for product_id in product_ids:
        view_product_in_batches(product_id, view_number, batch_size, proxy_manager)


if __name__ == '__main__':
    import argparse

    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description='Simulate product views.')
    parser.add_argument('--view-number', type=int, default=50, help='Number of views to simulate per product. Default [50]')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of concurrent views to run in each batch. Default [10]')
    parser.add_argument('--proxy-type', type=str, default='http', choices=['http', 'socks4', 'socks5'], help='The proxy type of connections. Default [http]')
    parser.add_argument('--proxy-test-type', type=str, default='', choices=['driver', 'request'], help='The type of proxy validation test. The driver mode takes more time but provides more accurate results, while the request mode is faster but offers less thorough validation. [If not passed, no test will be done]')
    args = parser.parse_args()

    # Automatically install the correct version of chromedriver
    chromedriver_autoinstaller.install()

    # Read product IDs from file
    product_ids = read_product_ids(ID_LIST_FILE)

    try:
        main(args.view_number, product_ids, args.batch_size, args.proxy_type, args.proxy_test_type)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
