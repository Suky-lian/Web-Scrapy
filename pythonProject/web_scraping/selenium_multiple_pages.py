from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time


# work silently using headless mode
# options = Options()
# options.headless = True
# options.add_argument('window-size=1920x1080')


web = 'https://web.archive.org/web/20211029194738/https://www.audible.com/adblbestsellers'
path = '/Users/lianjieting/Downloads/chromedriver-mac-arm64/chromedriver'  # write your path here
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service,options=Options)
driver.get(web)
driver.maximize_window()

# pagination
pagination = driver.find_element(by='xpath',value='//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(by='tag name',value='li')
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    time.sleep(2)
    container = driver.find_element(by='class name',value='adbl-impression-container ')
    products= container.find_elements(by='xpath',value='.//li[contains(@class, "productListItem")]')
    # Locator Type for find_element:
    # The valid locator types are id, name, class name, css selector, tag name, xpath, and link text.

    for product in products:
        book_title.append(product.find_element(by='xpath',value='.//h3[contains(@class,"bc-heading")]').text)
        book_author.append(product.find_element(by='xpath',value='.//li[contains(@class,"authorLabel")]').text)
        book_length.append(product.find_element(by='xpath',value='.//li[contains(@class,"runtimeLabel")]').text)

    current_page = current_page +1

    try:
        next_page = driver.find_element(by='xpath', value='//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass

# driver.quit()

#export data file
# df_books = pd.DataFrame({'Title':book_title,'author':book_author,'length':book_length})
# df_books.to_csv("book_headless.csv",index=False)