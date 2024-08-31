from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import shuffle
from requests import get, RequestException
from datetime import datetime
from os import path, makedirs

from src.utils import logger, read_file
from settings import VALID_PROXIES_PATH


class ProxyManager:
    def __init__(self, proxy_urls: list, proxy_type: str, test_url: str, test_type: str, proxy_file: str):
        """
        Initialize the ProxyManager class by fetching and shuffling proxies.

        Args:
            proxy_urls (list): A list of URLs to fetch proxies from.
        """
        self.lock = Lock()

        self.proxy_urls = proxy_urls
        self.proxy_type = proxy_type
        self.test_url = test_url
        if test_type:
            logger.info('Base on the fact that proxies are free, it may take time to test and use the valid one')
            logger.info('Start finding valid proxies...')
            self.__test_proxy = self.__test_proxy_driver if test_type == 'driver' else self.__test_proxy_request

        self.__ensure_valid_proxies_directory_exists()

        self.proxies = self.__fetch_valid_proxies(test_type, proxy_file)

    def __ensure_valid_proxies_directory_exists(self) -> None:
        """
        Ensures that the directory for storing valid proxies exists.
        Creates the directory if it does not exist.
        """
        if not path.exists(VALID_PROXIES_PATH):
            try:
                makedirs(VALID_PROXIES_PATH)
                logger.info(f"Created directory for valid proxies at {VALID_PROXIES_PATH}")
            except Exception as e:
                logger.error(f"Failed to create directory for valid proxies: {e}")

    def __fetch_valid_proxies(self, do_test: str, proxy_file: str) -> list:
        """
        Fetches proxy lists from the provided URLs or proxy file, deduplicates, shuffles, and returns them.

        Returns:
            list: A shuffled list of unique proxies.
        """
        proxies = read_file(proxy_file) if proxy_file else self.__online_fetch()
        proxies_list = self.__get_valid_proxies(list(proxies)) if do_test else list(proxies)

        return proxies_list

    def __online_fetch(self):
        proxies = set()

        for url in self.proxy_urls:
            try:
                response = get(url)
                response.raise_for_status()
                output = response.content.decode()

                if '\r\n' in output:
                    proxy_list = output.split('\r\n')
                else:
                    proxy_list = output.split('\n')

                for proxy in proxy_list:
                    if self.__is_valid_proxy_format(proxy.strip()):
                        proxies.add(proxy.strip())
                    else:
                        logger.debug(f"Invalid proxy format detected: {proxy.strip()}")


                proxies.update(filter(None, map(str.strip, proxy_list)))
            except RequestException as e:
                logger.error(f"Error fetching proxies from {url}: {e}")

        return proxies

    def __get_valid_proxies(self, proxy_list: list) -> list:
        """
        Tests proxies in parallel using a ThreadPoolExecutor.

        Args:
            proxies (list): A list of proxies to test.

        Returns:
            list: A list of valid proxies.
        """
        valid_proxies = []

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {executor.submit(self.__test_proxy, proxy): proxy for proxy in proxy_list}

            for future in as_completed(futures):
                proxy = futures[future]
                try:
                    if future.result():
                        valid_proxies.append(proxy)
                except Exception:
                    logger.debug(f"Error testing proxy {proxy}")

        shuffle(valid_proxies)
        self.__log_valid_proxies(valid_proxies)
        return valid_proxies

    def __log_valid_proxies(self, proxies: list) -> None:
        """
        Logs valid proxies to a file named 'valid_proxies_DATE_HOUR_MINUTE.txt'.

        Args:
            proxies (list): The list of valid proxies to log.
        """
        if not proxies:
            return

        # Create the file path using APP_PATH and current date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"valid_proxies_{current_time}.txt"
        file_path = path.join(VALID_PROXIES_PATH, filename)

        # Write the valid proxies to the file
        with self.lock:
            with open(file_path, 'a') as f:
                for proxy in proxies:
                    f.write(proxy + '\n')

        logger.debug(f"Logged {len(proxies)} valid proxies to {file_path}")

    def __is_valid_proxy_format(self, proxy: str) -> bool:
        """
        Checks if a proxy string is in the valid format of 'ip:port'.

        Args:
            proxy (str): The proxy string to validate.

        Returns:
            bool: True if the proxy format is valid, False otherwise.
        """
        parts = proxy.split(':')
        if len(parts) == 2:
            ip, port = parts
            if ip.count('.') == 3 and port.isdigit():
                return True
        return False

    def __test_proxy_driver(self, proxy: str) -> bool:
        """
        Tests a proxy by launching a WebDriver session and attempting to load a webpage.

        Args:
            proxy (str): The proxy to test, in the format 'ip:port'.

        Returns:
            bool: True if the proxy is valid for Selenium, False otherwise.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--proxy-server={self.proxy_type}://{proxy}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = None
        try:
            logger.debug(f"Proxy {proxy} is valid.")
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(6)
            driver.get(self.test_url)
            logger.debug(f"Proxy {proxy} is valid.")
            return True
        except Exception:
            logger.debug(f"Proxy {proxy} failed with WebDriver")
            return False
        finally:
            if driver:
                driver.close()
                driver.quit()

    def __test_proxy_request(self, proxy: str) -> bool:
        """
        Tests a proxy by making a request to a test URL.

        Args:
            proxy (str): The proxy to test, in the format 'ip:port'.

        Returns:
            bool: True if the proxy is valid, False otherwise.
        """
        try:
            proxies = {self.proxy_type: f"{self.proxy_type}://{proxy}"}
            response = get(self.test_url, proxies=proxies, timeout=5)

            # Consider proxy valid if status code is 200
            if response.status_code == 200:
                logger.debug(f"Proxy {proxy} is valid.")
                return True
            else:
                logger.debug(f"Proxy {proxy} returned status code {response.status_code}.")
                return False
        except RequestException as e:
            logger.debug(f"Proxy {proxy} failed with error: {e}")
            return False

    def get_random_proxy(self) -> str:
        """
        Returns a random valid proxy and removes it from the proxy list.

        Returns:
            str: A proxy in the format 'ip:port', or None if no valid proxies remain.
        """
        with self.lock:
            if self.proxies:
                return self.proxies.pop()
            
            logger.warn("No valid proxies available. Please fetch new proxies.")
            return None

    def refresh_proxies(self) -> None:
        """
        Refresh the list of proxies by fetching them again.
        """
        self.proxies = self.__fetch_valid_proxies()
