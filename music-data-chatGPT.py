import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Set up Chrome webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment this line if you want to run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

# Set up pandas dataframe
data = {
    'Track Name': [],
    'Artist Name': [],
    'Album Name': [],
    'Duration': []
}
df = pd.DataFrame(data)

# Define the number of pages and entries per page
num_pages = 5
entries_per_page = 25

# Iterate over each page
for page in range(1, num_pages + 1):
    url = f"https://app.lickd.co/search?from={((page-1) * entries_per_page)}&sortOrder=null&page=undefined"
    driver.get(url)

    # Scrape the data
    entries = driver.find_elements(By.CSS_SELECTOR, ".f7u2ugn")
    for entry in entries:
        track_name = entry.find_element(By.CSS_SELECTOR, "p.f9jey2b").text
        artist_name = entry.find_element(By.CSS_SELECTOR, "span.f45h.f63b58p").text
        album_name = entry.find_element(By.CSS_SELECTOR, "a[data-test-track-release='true']").text
        duration = entry.find_element(By.CSS_SELECTOR, "div.fnd9uo7 span").text

        # Check if the data is already in the dataframe
        if not any((df['Track Name'] == track_name) & (df['Artist Name'] == artist_name)):
            # Append data to pandas dataframe
            new_row = {
                'Track Name': track_name,
                'Artist Name': artist_name,
                'Album Name': album_name,
                'Duration': duration
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    print(f"Page {page} scraped.")

    # Click the next button
    next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next-button')]")
    driver.execute_script("arguments[0].click();", next_button)

    # Introduce a delay before scraping the next page
    time.sleep(1)  # Adjust the delay time (in seconds) as per your requirement

# Save the data to a CSV file
df.to_csv("chatgpt_data.csv", index=False)
print("Data saved to lickd_data.csv")

# Quit the webdriver
driver.quit()
