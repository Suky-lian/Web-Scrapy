
import os
# Ensure you are not in the numpy source directory
print("Current working directory:", os.getcwd())

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# define the website to scrape and path where the chromediver is located
website = 'https://x.com/i/flow/login'
path = '/Users/lianjieting/Downloads/chromedriver-mac-arm64/chromedriver'  # write your path here
service = Service(executable_path=path)  # selenium 4
driver = webdriver.Chrome(service=service)  # define 'driver' variable
# open Google Chrome with chromedriver
driver.get(website)
time.sleep(10)

# login = driver.find_element(by='xpath',value="//a[@href='/login']")
# login.click
# time.sleep(6)

# username = driver.find_element(by='xpath',value='//input[@autocomplete ="username"]')
username = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH, '//input[@autocomplete ="username"]')))
username.send_keys("sukylian")

next_button = driver.find_element(by='xpath',value='//button[@role="button"]//span[text()="Next"]')
next_button.click()
time.sleep(10)

# Wait for the password input to be clickable and enter the password
password = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]')))
password.send_keys("Jtlgoggo2022!!")

login_button = driver.find_element(by='xpath',value='//span[@class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"][text()="Log in"]')
login_button.click()

# Navigate to Twitter search page
search_term = 'Python'
search_url = f"https://x.com/search?q={search_term}&src=typed_query"
driver.get(search_url)
driver.maximize_window()
time.sleep(5)

# Function to scrape tweet data
def get_tweet(element):
    try:
        user = element.find_element(by='XPATH',value= ".//span[contains(text(), '@')]").text
        text = element.find_element(by='XPATH',value=".//div[@lang]").text
        tweets_data = [user, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data

# Initialize storage for tweet data
user_data = []
text_data = []
tweet_ids=set()

scrolling = True
while scrolling:
    # Get tweets from the search results page
    tweets = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    for tweet in tweets:
        tweets_data = get_tweet(tweet)
        tweet_id = ''.join(tweets_data)
        if tweet_id not in tweet_ids:
            tweet_ids.add((tweet_id))
            user_data.append(tweets_data[0])
            text_data.append(" ".join(tweets_data[1].split()))

    # infinite scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            scrolling = False # scrolling while look break
        else:
            last_height = new_height
            break

# Close the WebDriver
driver.quit()

# Save the data to a DataFrame and export to a CSV file
df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_infinite_scrolling.csv', index=False)
print(df_tweets)