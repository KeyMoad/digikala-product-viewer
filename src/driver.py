from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy


from src.utils import logger


class DriverManager:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager

    def get_driver(self):
        """
        Sets up the WebDriver with a random proxy from the ProxyManager.
        Handles both free and premium proxies.

        Returns:
            webdriver.Chrome: The configured WebDriver instance.
        """
        proxy = self.proxy_manager.get_random_proxy()
        proxy_type = self.proxy_manager.proxy_type
        username = self.proxy_manager.username
        password = self.proxy_manager.password

        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

        # Add the proxy to Chrome options
        if proxy:
            if self.proxy_manager.is_proxy_premium and username and password:
                proxy_url = f"{proxy_type}://{username}:{password}@{proxy}"
                proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)
                proxy_helper.enrich_chrome_options(chrome_options)
                logger.info(f"Using premium proxy [{proxy}] with auth via extension.")
            else:
                chrome_options.add_argument(f'--proxy-server={proxy_type}://{proxy}')
                logger.info(f'Using proxy [{proxy}] with [{proxy_type}] proxy type.')
        else:
            logger.warning('No proxy is being used')

        driver = webdriver.Chrome(options=chrome_options)
        return driver
