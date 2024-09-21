from signal import signal, SIGINT, SIGTERM
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.webdriver.support.ui import WebDriverWait
from sys import exit
from time import sleep
from random import uniform

from settings import BASE_PRODUCT_URL, DEFAULT_TIMEOUT, ID_LIST_FILE, HTTP_PROXY_LIST_URLS, SOCKS4_PROXY_LIST_URLS, SOCKS5_PROXY_LIST_URLS, DEFAULT_CONFIG_PATH, DATABASE_PATH
from src.config import load_config, merge_args_with_config
from src.utils import logger, read_file
from src.viewer import ProductViewer
from src.driver import DriverManager
from src.proxy import ProxyManager
from src.result import fetch_product_views, init_db


# Flag to indicate whether the script should keep running
keep_running = True

def handle_shutdown_signal(signum):
    """Handles shutdown signals to gracefully exit the script."""
    global keep_running
    logger.info(f"Received signal {signum}, shutting down gracefully. Be patient...")
    keep_running = False


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

    viewer = ProductViewer(driver, wait, DATABASE_PATH)
    viewer.simulate_views(url, 1, product_id)

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
        logger.info(f'{product_id.strip()} - Running batch {batch + 1}/{num_batches} with {current_batch_size} views...')

        with ThreadPoolExecutor(max_workers=current_batch_size) as executor:
            futures = [
                executor.submit(view_single_instance, product_id, proxy_manager)
                for _ in range(current_batch_size)
            ]

            for future in as_completed(futures):
                try:
                    future.result()  # This will raise an exception if the callable raised one
                except Exception as e:
                    logger.error(f"{product_id.strip()} - An error occurred while processing a view: {e}")

        if not (batch + 1) == num_batches:
            time_to_wait = uniform(15, 30)
            logger.info(f'{product_id.strip()} - Batch {batch + 1} completed. Waiting {time_to_wait} seconds...')
            sleep(time_to_wait)

    logger.info(f'Completed viewing process for product {product_id.strip()}')


def main(view_number: int, product_ids: list, batch_size: int, proxy_type: str, proxy_test_type: str, proxy_file: str, premium_proxy: bool, view_chunk: int, username: str = None, password: str = None):
    proxy_manager = ProxyManager(
        proxy_urls={
            'http': HTTP_PROXY_LIST_URLS,
            'socks4': SOCKS4_PROXY_LIST_URLS,
            'socks5': SOCKS5_PROXY_LIST_URLS
        }.get(proxy_type),
        proxy_type=proxy_type,
        test_url=BASE_PRODUCT_URL,
        test_type=proxy_test_type,
        proxy_file=proxy_file,
        premium=premium_proxy,
        username=username,
        password=password
    )

    if view_chunk == 0:
        # No chunking, process each product fully before moving to the next
        logger.info("No chunking specified. Processing all views for each product sequentially.")
        
        while keep_running:
            for product_id in product_ids:
                if not keep_running:
                    logger.info("Shutdown signal received. Exiting...")
                    break

                logger.info(f"Processing all {view_number} views for product {product_id.strip()}...")
                try:
                    view_product_in_batches(product_id, view_number, batch_size, proxy_manager)
                except Exception:
                    logger.error(f"Error during viewing process for product {product_id.strip()}.")
                
                proxy_manager.refresh_proxies()

            logger.info("All products viewed. Sleeping for 10 seconds...")
            sleep(10)

    else:
        # Chunking logic as before
        total_cycles = (view_number + view_chunk - 1) // view_chunk if view_chunk > 0 else 1

        while keep_running:
            current_cycle = 0
            while current_cycle < total_cycles and keep_running:
                logger.info(f"Starting cycle {current_cycle + 1}/{total_cycles}...")

                for product_id in product_ids:
                    if not keep_running:
                        logger.info("Shutdown signal received. Exiting...")
                        break

                    views_in_current_cycle = min(view_chunk, view_number - current_cycle * view_chunk)
                    logger.info(f"Processing {views_in_current_cycle} views for product {product_id.strip()}...")
                    
                    try:
                        view_product_in_batches(product_id, views_in_current_cycle, batch_size, proxy_manager)
                    except Exception:
                        logger.error(f"Error during viewing process for product {product_id.strip()}.")
                    
                    proxy_manager.refresh_proxies()

                current_cycle += 1

            logger.info("All products viewed for this cycle. Sleeping for 10 seconds before the next cycle...")
            sleep(10)


if __name__ == '__main__':
    from argparse import ArgumentParser
    import chromedriver_autoinstaller

    # Argument parser for command line arguments
    parser = ArgumentParser(description='Simulate product views.')
    parser.add_argument('--result', type=str, nargs='?', const='all', help='Display the completed views.')
    parser.add_argument('--config', type=str, default=DEFAULT_CONFIG_PATH, help='Path to the config file.')
    parser.add_argument('--view-number', type=int, help='Number of views to simulate per product. Default [50]')
    parser.add_argument('--batch-size', type=int, help='Number of concurrent views to run in each batch. Default [10]')
    parser.add_argument('--proxy-type', type=str, choices=['http', 'socks4', 'socks5'], help='The proxy type of connections. Default [http]')
    parser.add_argument('--proxy-test-type', type=str, choices=['driver', 'request'], help='The type of proxy validation test. The driver mode takes more time but provides more accurate results, while the request mode is faster but offers less thorough validation. [If not passed, no test will be done]')
    parser.add_argument('--proxy-file', type=str, help='If you want to use your own proxy list, pass the file path. File format should be txt and put your proxies addresses with this syntax: IP:PORT. [proxy-type is necessary]')
    parser.add_argument('--premium-proxy', action='store_true', help='If passed, indicates that the proxy list contains premium proxies.')
    parser.add_argument('--username', type=str, help='Username for premium proxy authentication.')
    parser.add_argument('--password', type=str, help='Password for premium proxy authentication.')
    parser.add_argument('--view-chunk', type=int, help='Number of views per chunk for each product. Default is to distribute views evenly across products.')

    args = parser.parse_args()

    # If --result is passed, display the product views
    if args.result:
        if args.result == 'all':
            all_views = fetch_product_views(DATABASE_PATH)
            if all_views:
                for record in all_views:
                    print(f"Product: {record[0]} | Completed Views: {record[1]}")
            else:
                print(f"No records found.")
        else:
            product_view = fetch_product_views(DATABASE_PATH, product_id=args.result)
            if product_view:
                print(f"Product: {product_view[0]} | Completed Views: {product_view[1]}")
            else:
                print(f"No records found for product {args.result}.")
        exit(0)

    # Read product IDs from file
    product_ids = read_file(ID_LIST_FILE)
    if not product_ids:
        logger.error(f'Please add your Product IDs in {ID_LIST_FILE} file.')
        exit(1)

    # Initialize database
    init_db(db_path=DATABASE_PATH, product_id_list=product_ids)

    # Load config file
    config = load_config(args.config)
    # Merge arguments with config values
    merged_args = merge_args_with_config(args, config)

    # Automatically install the correct version of chromedriver
    chromedriver_autoinstaller.install()

    # Validate necessary arguments
    if merged_args['premium_proxy'] and (not merged_args['proxy_file']):
        logger.error('Please provide premium proxy list as a file.')
        exit(1)
    if merged_args['premium_proxy'] and (not merged_args['username'] or not merged_args['password']):
        logger.error('Premium proxy requires both a username and a password.')
        exit(1)
    if merged_args['view_chunk'] > merged_args['view_number']:
        logger.error('View Chunk must be smaller than view number.')
        exit(1)

    signal(SIGINT, handle_shutdown_signal)   # Handle Ctrl+C
    signal(SIGTERM, handle_shutdown_signal)  # Handle service termination

    try:
        main(
            merged_args['view_number'],
            product_ids,
            merged_args['batch_size'],
            merged_args['proxy_type'],
            merged_args['proxy_test_type'],
            merged_args['proxy_file'],
            merged_args['premium_proxy'],
            merged_args['view_chunk'],
            merged_args['username'],
            merged_args['password']
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
