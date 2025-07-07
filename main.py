import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def dump_jobs():
    print("🚀 Launching undetected Chrome (non-headless)…")

    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/138.0.7204.51 Safari/537.36")

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"❌ Failed to launch Chrome:\n→ {e}")
        return

    try:
        job_title = input("Job title (e.g., sales rep): ").strip()
        location = input("Location (city, state or zip, e.g., Newark NJ): ").strip()
        keywords = input("Additional keywords (optional, e.g., remote, $60k): ").strip()

        query = f"{job_title} {location} {keywords}".strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={query}&udm=8"

        print(f"🔍 Searching jobs at:\n{url}\n")
        driver.get(url)

        print("⏳ Waiting 3 seconds for page to load or CAPTCHA to appear…")
        time.sleep(3)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "a.MQUd2b")
        if not job_cards:
            print("❌ No job cards found. CAPTCHA might be active or page layout changed.")
        else:
            print("✅ Listing jobs:\n")
            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "div.tNxQIb.PUpOsf").text
                    company = card.find_element(By.CSS_SELECTOR, "div.wHYlTd.MKCbgd.a3jPc").text
                    location = card.find_element(By.CSS_SELECTOR, "div.wHYlTd.FqK3wc.MKCbgd").text
                    print(f"🧾 {title} — {company} — {location}")
                except Exception:
                    pass  # Skip broken cards

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user.")

    except Exception as e:
        print(f"❌ Unexpected error:\n→ {e}")

    finally:
        input("\nPress Enter to close browser...")
        try:
            driver.quit()
        except:
            pass
        print("Browser closed.")

if __name__ == "__main__":
    dump_jobs()
