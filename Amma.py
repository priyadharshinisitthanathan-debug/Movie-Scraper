import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.imdb.com/chart/top/"
driver.get(url)
time.sleep(4)

movies = []
years = []
ratings = []
ranks = []

rows = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

print("Movies found:", len(rows))

for idx, row in enumerate(rows, start=1):
    try:
        # Title
        title = row.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.strip()

        # Year
        year = row.find_element(By.CSS_SELECTOR, "span.cli-title-metadata-item").text.strip()

        # Rating
        rating = row.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text.strip()

        # Rank (manual)
        rank = idx

        movies.append(title)
        years.append(year)
        ratings.append(rating)
        ranks.append(rank)

    except Exception as e:
        print("Skipping row due to:", e)
        continue

# Create DataFrame
df = pd.DataFrame({
    "Rank": ranks,
    "Movie Title": movies,
    "Year": years,
    "IMDb Rating": ratings
})

df.to_csv("imdb_top_250.csv", index=False)

print("\nSUCCESS! → imdb_top_250.csv created 🎉")

driver.quit()