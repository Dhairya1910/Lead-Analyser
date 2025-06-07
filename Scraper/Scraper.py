from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

""" from scraping data from google Maps based on location """

def google_maps_scraper(industry, location, max_results=20):
    options = Options()
    options.add_argument("--start-maximized") # this is the for demo to show how searching takes place on chrome  
    # options.add_argument("--start-minimized") 
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 15)

    # Go to Google Maps
    driver.get("https://www.google.com/maps")

    # Search input
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search_box.send_keys(f"{industry} industry in {location}")
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    # Scroll inside the search results container
    scrollable_div = wait.until(EC.presence_of_element_located((
        By.XPATH, '//div[contains(@aria-label, "Results for") and @role="feed"]')))
    prev_count = 0
    scroll_attempts = 0

    while True:
        # Scroll the container
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(2)

        results = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        current_count = len(results)

        if current_count >= max_results or scroll_attempts >= 10:
            break

        if current_count == prev_count:
            scroll_attempts += 1
        else:
            scroll_attempts = 0
            prev_count = current_count

    print(f"Found {len(results)} result cards")

    data = []
    seen_names = set()

    for index, result in enumerate(results[:max_results]):
        try:
            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", result)
            ActionChains(driver).move_to_element(result).click().perform()
            time.sleep(4)

            name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf"))).text
            if name in seen_names:
                continue
            seen_names.add(name)

            try:
                address = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div/div[2]/div[1]').text
            except:
                address = "NA"

            try:
                phone = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[7]/button/div/div[2]/div[1]').text
            except:
                phone = "NA"

            try:
                website = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[6]/a/div/div[2]/div[1]').text
            except:
                website = "NA"

            try:
                rating = driver.find_element(By.CLASS_NAME, "MW4etd").text
            except:
                rating = "NA"

            data.append({
                "Company": name,
                "Industry": industry,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Location": location
            })

            print(f"[{index+1}] Scraped: {name}")

        except Exception as e:
            print(f"[{index+1}] Error: {e}")
            continue

    driver.quit()

    df = pd.DataFrame(data)
    filename = f"{industry.replace(' ', '_')}_in_{location.replace(' ', '_')}_maps_leads.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved {len(data)} leads to '{filename}'")
    return df
