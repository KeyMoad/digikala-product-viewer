from os import path


# App Path
APP_PATH = path.dirname(path.realpath(__file__))

# Define the product URL
BASE_PRODUCT_URL = 'https://www.digikala.com/product'
DEFAULT_TIMEOUT = 10

# Proxy list
HTTP_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt',
    'https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt'
]
SOCKS4_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt'
]
SOCKS5_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt'
]

# Default config file path
DEFAULT_CONFIG_PATH = path.join(APP_PATH, 'config.yaml')

# ID List file path
ID_LIST_FILE = path.join(APP_PATH, 'id_list.txt')

# Valid Proxies Path
VALID_PROXIES_PATH = path.join(APP_PATH, 'valid_proxies')

# Database Path
DATABASE_PATH = path.join(APP_PATH, 'views.db')
