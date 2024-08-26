from os import path


# Define the product URL
BASE_PRODUCT_URL = 'https://www.digikala.com/product'
DEFAULT_TIMEOUT = 10

# Proxy list
HTTP_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt'
    
]
SOCKS4_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks4_proxies.txt'
]
SOCKS5_PROXY_LIST_URLS = [
    'https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt',
    'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/socks5_proxies.txt'
]

# ID List file path
ID_LIST_FILE = path.join(path.dirname(path.realpath(__file__)), 'id_list.txt')
