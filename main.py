from selenium import webdriver
from selenium.webdriver.common.by import By
import re

GROWTH_IN_CLICKS_BEFORE_NEXT_CLICK_PASS = 1.03

def click_on_cookie(seldriver, num_clicks):
    elem_cookie_btn = seldriver.find_element(By.ID, "bigCookie")
    for n in range(0, num_clicks):
        try:
            elem_cookie_btn.click()
        except Exception:
            # selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted:
            # Element < button id = "bigCookie" > < / button > is not clickable
            # at zpoint(206, 539).
            #
            # Other element would receive the click:
            # < div class ="shimmer" alt="Golden cookie" style="left: 115px; top: 434px; width: 96px; height: 96px; background-image: url(&quot;img/goldCookie.png&quot;); background-position: 0px 0px; opacity: 0.865912; display: block; transform: rotate(-13.7111deg) scale(1.03691);" > < / div >
            #
            # (Session info: chrome=141.0.7390.107);
            # For documentation on this error, please
            # visit: https: // www.selenium.dev / documentation / webdriver / troubleshooting / errors  # elementclickinterceptedexception
            driver.implicitly_wait(.1)

def get_num_cookies(seldriver):
    try:
        elem_num_cookies = seldriver.find_element(By.ID, "cookies")
        match = re.search(r'(\d{1,3}(?:,\d{3})*)', elem_num_cookies.text)
        if match:
            # Remove commas and convert to int
            return int(match.group(1).replace(',', ''))
    except Exception:
        pass
    return None

# keep the browser open after opening it
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# open up a chrome browser and navigate to the cookie page
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
driver.get("https://ozh.github.io/cookieclicker/")

# allow the page to load
driver.implicitly_wait(2)

# click on the language
elem_english_lang_btn = driver.find_element(By.ID, "langSelect-EN")
elem_english_lang_btn.click()
driver.implicitly_wait(2)

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
            most_expensive_upgrade.click()
            print(f"You just purchased {most_expensive_upgrade.text}")
    except Exception:
        print("ignoring exception")

    clicks_before_buy = int(clicks_before_buy * GROWTH_IN_CLICKS_BEFORE_NEXT_CLICK_PASS)
    print(f"Waiting {clicks_before_buy} clicks until next purchase attempt")


# close the browser when we're done using it
#driver.close() # closes the active tab
#driver.quit() # closes the entire browser
time.sleep(1000)