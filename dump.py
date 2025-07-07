import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

search_query = "driver jobs in Newark NJ"
output_file = "data.html"

def main():
    print("Launching browser with undetected-chromedriver...")

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    driver = uc.Chrome(options=options)
    driver.get(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")

    try:
        print("Waiting for Google job panel to load...")

        # Wait for real job cards (inside Google's jobs widget)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jscontroller="Q7Rsec"]'))
        )

        job_cards = driver.find_elements(By.CSS_SELECTOR, 'div[jscontroller="Q7Rsec"]')
        print(f"✅ Found {len(job_cards)} job cards.")

        for idx, card in enumerate(job_cards[:20], 1):  # max 20 jobs
            try:
                title = card.find_element(By.CSS_SELECTOR, 'div[role="heading"]').text
            except:
                title = "N/A"
            try:
                company = card.find_element(By.CSS_SELECTOR, 'div.sHb2Xb').text
            except:
                company = "N/A"
            try:
                location = card.find_element(By.CSS_SELECTOR, 'div.Qk80Jf').text
            except:
                location = "N/A"
            try:
                link = card.find_element(By.XPATH, ".//a").get_attribute("href")
            except:
                link = "N/A"

            print(f"\nJob #{idx}")
            print(f"Title   : {title}")
            print(f"Company : {company}")
            print(f"Location: {location}")
            print(f"Link    : {link}")

        with open(output_file, "w", encoding="utf-8") as f:
            for card in job_cards[:20]:
                f.write(card.get_attribute("outerHTML") + "\n")

        print(f"\n✅ Saved {len(job_cards[:20])} job cards HTML to {output_file}")

    except Exception as e:
        print("\n❌ Error occurred — likely Google blocked the widget or changed structure.")
        print(f"Error: {e}")

    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
