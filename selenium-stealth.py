from selenium import webdriver
from selenium_stealth import stealth
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")

# Initialize the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)

# Apply stealth settings to the browser
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
        )

# Open Bull Market login page
driver.get("https://bullmarketbrokers.com")
time.sleep(150)  # Wait for manual login

# Once logged in manually, proceed to the account balance page
driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
time.sleep(5)

# Perform actions, e.g., download files or scrape data
# Add your scraping code here, similar to your previous script

driver.quit()
