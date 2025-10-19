from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

def click_on_cookie(seldriver, num_clicks):
    elem_cookie_btn = seldriver.find_element(By.ID, "bigCookie")
    for n in range(0, num_clicks):
        elem_cookie_btn.click()

def get_num_cookies(seldriver):
    elem_num_cookies = seldriver.find_element(By.ID, "cookies")
    match = re.search(r'(\d{1,3}(?:,\d{3})*)', elem_num_cookies.text)
    if match:
        # Remove commas and convert to int
        return int(match.group(1).replace(',', ''))
    return None

# keep the browser open after opening it
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# open up a chrome browser and navigate to the cookie page
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
driver.get("https://ozh.github.io/cookieclicker/")

# allow the page to load
time.sleep(2)

# click on the language
elem_english_lang_btn = driver.find_element(By.ID, "langSelect-EN")
elem_english_lang_btn.click()
time.sleep(1)

# begin clicking on the cookie
clicks_before_buy = 100
while True:
    click_on_cookie(driver, clicks_before_buy)

    # attempt to buy the most expensive item in the shop; it's possible nothing may be available since we're low on cash
    try:
        upgrades = driver.find_elements(By.CSS_SELECTOR, value=".product.unlocked.enabled")
        most_expensive_upgrades_index = len(upgrades) - 1
        most_expensive_upgrade = driver.find_element(By.ID, value=f"product{most_expensive_upgrades_index}")
        if most_expensive_upgrade is not None:
            num_cookies = get_num_cookies(driver)
            print(f"You currently have {num_cookies} cookies")
            most_expensive_upgrade.click()
            print(f"You just purchased {most_expensive_upgrade.text}")
    except Exception:
        print("ignoring exception")

    num_cookies = get_num_cookies(driver)
    clicks_before_buy = int(clicks_before_buy * 1.015)
    print(f"You now have {num_cookies} cookies; waiting {clicks_before_buy} clicks until next purchase attempt")


# close the browser when we're done using it
#driver.close() # closes the active tab
#driver.quit() # closes the entire browser
time.sleep(1000)