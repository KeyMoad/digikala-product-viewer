# Digikala Product Viewer Script

## **Overview**

This script automates the simulation of product page views using proxies to mimic real user behavior. It's designed for situations where you want to generate traffic to specific product pages without being blocked by rate limits or IP restrictions. It leverages Selenium WebDriver for browser automation, allowing for randomized browsing patterns, including scrolling and clicking on various product tabs.

## **Features**

- **Automated Viewing**: Simulate multiple views on a Digikala product page.
- **Proxy Support**: Supports HTTP, SOCKS4, and SOCKS5 proxies. You can either fetch proxies from predefined URLs or provide your own list.
- **Concurrency**: Simulates multiple concurrent views using `ThreadPoolExecutor`.
- **Randomized User Interaction**: Implements random delays, scrolling, and clicks to mimic human behavior.
- **Proxy Validation**: Optionally validates proxies before use to ensure they are working.
- **Headless Operation**: Runs Chrome in headless mode for efficiency.

## **File Structure**

- **`main.py`**: The main script where the viewing process is initiated.
- **`settings.py`**: Contains configurations such as base URLs, file paths, and default timeout settings.
- **`src/utils.py`**: Utility functions for logging and reading files.
- **`src/viewer.py`**: Contains the logic for simulating user interactions on the product page.
- **`src/driver.py`**: Manages WebDriver instances and integrates proxies.
- **`src/proxy.py`**: Manages proxy fetching, testing, and allocation.

## **Requirements**

- Python 3.8+
- Selenium
- `chromedriver_autoinstaller` (automatically installs the correct version of ChromeDriver)
- `requests` for fetching proxies

## **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KeyMoad/digikala-product-viewer.git
   cd digikala-product-viewer
   ```

2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chromedriver Setup**:
   The script uses `chromedriver_autoinstaller` to automatically install the appropriate version of ChromeDriver, so no additional setup is required.

## **Usage**

You can run the script from the command line with various arguments to control its behavior.

### **Basic Command**

```bash
python main.py --view-number 50 --batch-size 10 --proxy-type http
```

### **Arguments**

- **`--view-number`**: The number of views to simulate per product. Default is 50.
- **`--batch-size`**: The number of concurrent views to run in each batch. Default is 10.
- **`--proxy-type`**: Type of proxy to use (options: `http`, `socks4`, `socks5`). Default is `http`.
- **`--proxy-test-type`**: Optional. Type of proxy validation test (`driver` or `request`). If not provided, no validation is performed.
- **`--proxy-file`**: Optional. Path to a file containing custom proxy addresses. If not provided, proxies will be fetched online.

### **Example Command**

```bash
python main.py --view-number 100 --batch-size 20 --proxy-type socks5 --proxy-test-type request --proxy-file proxies.txt
```

This command simulates 100 views per product, with 20 concurrent views at a time using SOCKS5 proxies. The proxies will be validated using the `request` method and loaded from the `proxies.txt` file.

## **Customizing Behavior**

- **Timeout Settings**: Modify `DEFAULT_TIMEOUT` in `settings.py` to change how long the script waits for elements.
- **Product URL**: The `BASE_PRODUCT_URL` in `settings.py` defines the root URL for the products you want to view.
- **Product IDs**: Ensure your product IDs are listed in a text file, with each ID on a new line. The file path is set in `ID_LIST_FILE` in `settings.py`.

## **Logging**

All activities are logged, including proxy validation results and any errors encountered during the viewing process. Logs can be found in the console output.

## **Caution**

- **Ethical Use**: Ensure that the use of this tool complies with the website's terms of service and legal regulations.
- **Proxy Quality**: Free proxies can be unreliable. Consider using high-quality proxies for consistent performance.

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
