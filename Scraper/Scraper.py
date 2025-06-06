from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def google_maps_scraper(industry, location, max_results=20):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com/maps")
    
    wait = WebDriverWait(driver, 10)

    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search_box.send_keys(f"{industry} industry in {location}")
    search_box.send_keys(Keys.ENTER)
    
    time.sleep(5)

    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    results = driver.find_elements(By.CLASS_NAME, "Nv2PK")[:max_results]
    data = []

    for result in results:
        try:
            result.click()
            time.sleep(4)

            name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "DUwDvf"))).text
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
                "Name": name,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Rating": rating,
            })

        except Exception as e:
            print("Error with one result:", e)
            continue

    driver.quit()
    df = pd.DataFrame(data)
    df.to_csv(f"{industry}_in_{location}_maps_leads.csv", index=False)
    return df


df = google_maps_scraper("Artificial Intelligence", "Pune", max_results=10)
print(df)
