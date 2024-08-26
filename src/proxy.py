from random import shuffle
from requests import get, RequestException
from src.utils import logger


class ProxyManager:
    def __init__(self, proxy_urls: list, proxy_type: str):
        """
        Initialize the ProxyManager class by fetching and shuffling proxies.

        Args:
            proxy_urls (list): A list of URLs to fetch proxies from.
        """
        self.proxy_urls = proxy_urls
        self.proxies = self.fetch_proxies()
        self.proxy_type = proxy_type

    def fetch_proxies(self) -> list:
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

                proxies.update(filter(None, map(str.strip, proxy_list)))
            except RequestException as e:
                logger.error(f"Error fetching proxies from {url}: {e}")

        proxies_list = list(proxies)
        shuffle(proxies_list)
        return proxies_list

    def get_random_proxy(self) -> str:
        """
        Returns a random proxy and removes it from the proxy list.

        Returns:
            str: A proxy in the format 'ip:port'.
        """
        if not self.proxies:
            logger.warn("No proxies available. Please fetch new proxies.")
            return None

        proxy = self.proxies.pop()
        return proxy

    def refresh_proxies(self) -> None:
        """
        Refresh the list of proxies by fetching them again.
        """
        self.proxies = self.fetch_proxies()
