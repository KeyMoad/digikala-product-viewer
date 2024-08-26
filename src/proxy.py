from random import shuffle
from requests import get, RequestException
from src.utils import logger


class ProxyManager:
    def __init__(self, proxy_urls: list, proxy_type: str, test_url: str):
        """
        Initialize the ProxyManager class by fetching and shuffling proxies.

        Args:
            proxy_urls (list): A list of URLs to fetch proxies from.
        """
        self.proxy_urls = proxy_urls
        self.proxy_type = proxy_type
        self.proxies = self.__fetch_proxies()
        self.test_url = test_url

    def __fetch_proxies(self) -> list:
        """
        Fetches proxy lists from the provided URLs, deduplicates, shuffles, and returns them.

        Returns:
            list: A shuffled list of unique proxies.
        """
        proxies = set()

        for url in self.proxy_urls:
            try:
                response = get(url)
                response.raise_for_status()  # Ensure we notice bad responses
                output = response.content.decode()

                if '\r\n' in output:
                    proxy_list = output.split('\r\n')
                else:
                    proxy_list = output.split('\n')

                # Ensure proxies are in a valid format (ip:port)
                for proxy in proxy_list:
                    if self.__is_valid_proxy_format(proxy.strip()):
                        proxies.add(proxy.strip())
                    else:
                        logger.debug(f"Invalid proxy format detected: {proxy.strip()}")


                proxies.update(filter(None, map(str.strip, proxy_list)))
            except RequestException as e:
                logger.error(f"Error fetching proxies from {url}: {e}")

        proxies_list = list(proxies)
        shuffle(proxies_list)
        return proxies_list

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

    def __test_proxy(self, proxy: str) -> bool:
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
            str: A proxy in the format 'ip:port'.
        """
        while self.proxies:
            proxy = self.proxies.pop()

            if self.__test_proxy(proxy):
                return proxy

        logger.warn("No valid proxies available. Please fetch new proxies.")
        return None

    def refresh_proxies(self) -> None:
        """
        Refresh the list of proxies by fetching them again.
        """
        self.proxies = self.__fetch_proxies()
