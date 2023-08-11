import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=headset&crid=395K4R54QEGAY&sprefix=headset%2Caps%2C299&ref=nb_sb_noss_1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
headset_cards = soup.find_all("div", class_="s-result-item")

headset_data = []

for headset_card in headset_cards:
    try:
        headset_name = headset_card.find("span", class_="a-text-normal").text.strip()
        headset_price = headset_card.find("span", class_="a-offscreen").text if headset_card.find("span", class_="a-offscreen") else "N/A"
        headset_rating = headset_card.find("span", class_="a-icon-alt").text if headset_card.find("span", class_="a-icon-alt") else "N/A"
        
        headset_data.append({
            "Name": headset_name,
            "Price": headset_price,
            "Rating": headset_rating
        })
    except Exception as e:
        print("Error in extracting headset data:", e)

df = pd.DataFrame(headset_data)
df.to_csv("amazon_Headsets.csv", index=False)

print("Data successfully extracted and CSV saved.")
