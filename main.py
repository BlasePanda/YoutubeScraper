import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.chrome.options import Options


# Set up logging
import logging
logging.basicConfig(filename='scraper.log', level=logging.DEBUG)

url = "youtube_url_page_you_want_to_scrap"


channel_id = url.split('/')[4]

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome() #(options=options)
driver.get(url)
time.sleep(random.randint(3, 8))
dejtajm = datetime.datetime.now().strftime("%Y%m%d%H%M")
height = driver.execute_script("return document.documentElement.scrollHeight")
lastheight = 0

# If you don't have the Youtube cookie pop-up window issue, you can comment the following codes.
consent_button_xpath = "//button[@aria-label='Reject all']"
consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))
consent = driver.find_element("xpath", consent_button_xpath)
consent.click()


while True:
    if lastheight == height:
        break
    lastheight = height
    logging.debug(f'Page height: {lastheight}')
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #Try scrolling with this
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")
    time.sleep(2)
    height = driver.execute_script("return document.documentElement.scrollHeight")
# try just appending user data to text file without going through ever line
user_urls = driver.find_elements('xpath', '//*[@id="video-title-link"]')
user_data = driver.find_elements('xpath', '//*[@id="video-title"]')
# # For shorts
# user_data = driver.find_elements('xpath', '//*[@class="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-slim-media"]')
# user_urls = driver.find_elements('xpath', '//*[@class="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-slim-media"]')

for i, j in zip(user_urls, user_data):
    url = i.get_attribute('href')
    link = j.get_attribute('aria-label')
    print(f'{link} ({url})')
    with open(channel_id + dejtajm + '.txt', 'a+', encoding='utf8') as file:
        file.write(f'{link} ({url})\n')

driver.quit()

logging.info('Scraping successful')
