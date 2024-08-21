from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from random import randint, uniform
import chromedriver_autoinstaller

# Automatically install the correct version of chromedriver
chromedriver_autoinstaller.install()

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Define the product URL
product_url = 'https://www.digikala.com/product/dkp-7439603/'  # Replace with the test product URL

# Number of views to simulate
number_of_views = 3

# Wait for elements to be available (timeout after 10 seconds)
wait = WebDriverWait(driver, 10)

def scroll_and_click(selector, max_scrolls=5):
    for _ in range(max_scrolls):
        try:
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            driver.execute_script("window.scrollBy(0, 400);")
            sleep(1)
    return False

for i in range(number_of_views):
    driver.get(product_url)
    sleep(uniform(2, 5))

    for _ in range(randint(4, 7)):
        scroll_amount = randint(200, 1000)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        sleep(uniform(0.5, 1.5))

    try:
        review_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
        if scroll_and_click(review_tab_selector):
            print("Clicked on First button")
        sleep(uniform(2, 6))

        specs_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-subtitle.text-neutral-500.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
        if scroll_and_click(specs_tab_selector):
            print("Clicked on Second button")
        sleep(uniform(1, 3))

        comments_tab_selector = "li.relative.px-4.py-2.flex.flex-row.items-center.grow.justify-center.lg\\:grow-0.text-primary-500.text-subtitle-strong.cursor-pointer.text-body2-strong.flex.min-w-fit.max-w-\\[300px\\].lg\\:max-w-\\[400px\\].overflow-hidden[data-cro-id='pdp-scroll-menu']"
        if scroll_and_click(comments_tab_selector):
            print("Clicked on Third button")
        sleep(uniform(2, 5))

        see_all_comments_selector = "span.inline-flex.items-center.cursor-pointer.styles_Anchor--secondary__3KsgY.text-button-2.my-auto"
        if scroll_and_click(see_all_comments_selector):
            print("Clicked on Last button")
        sleep(uniform(4, 7))

    except Exception as e:
        print(f"Could not complete the interaction: {e}")

    # Scroll back up
    driver.execute_script("window.scrollTo(0, 0);")
    sleep(uniform(1, 3))  # Random delay after scrolling back

    print(f"View {i+1} completed")

driver.quit()  # Close the browser when done
