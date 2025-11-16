import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# === Load CSV ===
df = pd.read_csv("avito_scraped_data1.csv")

# === Setup WebDriver ===
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# === Loop through listings and extract number of rooms ===
rooms_list = []

for i, link in enumerate(df["link"][:10]):
    try:
        driver.get(link)
        time.sleep(2)  # wait for page to load

        # Find divs and look for the one with "Chambres"
        divs = driver.find_elements(By.TAG_NAME, "div")
        room = None

        for div in divs:
            text = div.text
            if "Chambres" in text:
                # Extract just the number (right of ":")
                parts = text.split(":")
                if len(parts) > 1:
                    room = parts[1].strip()
                else:
                    room = text.strip()
                break

        rooms_list.append(room)
        print(f"{i+1}/{len(df)} ✅ {room}")

    except Exception as e:
        print(f"{i+1}/{len(df)} ❌ Error: {e}")
        rooms_list.append(None)

# === Add to DataFrame ===
df["rooms"] = rooms_list

# === Save updated CSV ===
df.to_csv("avito_updated_with_rooms.csv", index=False)
print("✅ Done! Saved as avito_updated_with_rooms.csv")

# === Close browser ===
driver.quit()
