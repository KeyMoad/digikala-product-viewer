# Digikala Product Viewer Script

This Python script simulates multiple views on product pages on Digikala using Selenium WebDriver. It automates interactions with the product pages to mimic user behavior, such as scrolling and clicking on various tabs.

## Features

- **Automated Viewing**: Simulate multiple views on a Digikala product page.
- **Dynamic Interaction**: Automatically scrolls through the page and interacts with various elements like review tabs, specifications, and comments.
- **Headless Operation**: Runs Chrome in headless mode for efficiency.

## Requirements

- Python 3.6+
- Selenium
- ChromeDriver (automatically managed by `chromedriver_autoinstaller`)

## Installation

1. **Clone the Repository**

   ```bash
   git https://github.com/KeyMoad/digikala-product-viewer.git
   cd digikala-product-viewer
   ```

2. **Install Dependencies**

   Make sure you have Python and pip installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should contain:

   ```
    attrs
    beautifulsoup4
    certifi
    charset-normalizer
    chromedriver-autoinstaller
    h11
    idna
    outcome
    packaging
    PySocks
    requests
    selenium
    sniffio
    sortedcontainers
    soupsieve
    trio
    trio-websocket
    typing_extensions
    urllib3
    websocket-client
    wsproto
   ```

## Usage

1. **Prepare the Script**

   Make sure you have the `chromedriver_autoinstaller` package installed. This will automatically manage the correct version of ChromeDriver for your system.

2. **Run the Script**

   Execute the script from the command line:

   ```bash
   python main.py
   ```

   You will be prompted to enter the following:

   - **Product IDs**: Enter the product IDs separated by commas.
   - **Number of Views**: Enter the number of views to simulate for each product.

   Example input:

   ```
   Enter product IDs separated by commas: dkp-12345, dkp-67890
   Enter the number of views: 10
   ```

## How It Works

1. **Initialization**: The script initializes a Chrome WebDriver instance with headless mode enabled.

2. **Product Viewing**: For each product ID provided:
   - The script navigates to the product page.
   - Simulates user interactions such as scrolling and clicking on review tabs, specifications, and comments.
   - Randomizes delays between actions to mimic human behavior.

3. **Error Handling**: Logs warnings and errors if elements cannot be interacted with or if other issues occur during execution.

## Example

Below is a sample output of the script:

```
2024-08-21 12:00:00 - INFO - Checking product dkp-12345 [https://www.digikala.com/product/dkp-12345] ...
2024-08-21 12:00:05 - INFO - Clicked on Review tab
2024-08-21 12:00:15 - INFO - Clicked on Specs tab
2024-08-21 12:00:20 - INFO - Clicked on Comments tab
2024-08-21 12:00:25 - INFO - Clicked on See All Comments
2024-08-21 12:00:30 - INFO - View 1 completed
...
```

## Notes

- **Selectors**: CSS selectors used in the script may need to be updated if Digikala changes its page layout or element identifiers.
- **Headless Mode**: The script runs in headless mode for efficiency. If you need to see the browser interaction, remove the `--headless` option from the Chrome options.

## Contributing

Feel free to contribute by opening issues or submitting pull requests. Please ensure to follow the contribution guidelines and maintain code quality.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
