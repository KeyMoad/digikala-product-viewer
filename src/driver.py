from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# Function to setup WebDriver with a random proxy
def get_driver(proxy, proxy_type):
    us = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-agent={us}")

    # Add the proxy to Chrome options
    chrome_options.add_argument(f'--proxy-server={proxy_type}://{proxy}')

    driver = webdriver.Chrome(options=chrome_options)
    return driver
