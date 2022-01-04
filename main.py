from utils.db import insert_into, does_id_exist
from utils.email_sender import send_email
import config

import os
os.chdir(r"C:\Users\jlcal\Desktop\Projects\craigslist-room-share-scrapper")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import airbnb
import re

DRIVER_PATH = "driver\chromedriver.exe"
print(os.path.dirname(os.getcwd()))
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')
# chrome_options.headless = True # also works

driver = webdriver.Chrome(executable_path=str(DRIVER_PATH),options=chrome_options)
driver.get('https://newjersey.craigslist.org/search/hhh?lat=40.99104221112936&lon=-74.33555603027345&excats=2-17-21-1-17-7-34-22-22-1&search_distance=4&max_price=1500&availabilityMode=0&sale_date=all+dates')

soup = BeautifulSoup(driver.page_source,'html.parser')


def clean_the_string(element):
    if element:
        text = element.getText().strip().title()
    else:
        text = ''
    return text


towns = config.towns
craig_entries = []

for item in soup.select('#search-results li'):
    pid = item.attrs['data-pid']
    name = clean_the_string(item.find('h3'))
    hood = re.search(r"(?<=\().+?(?=\))",str(item.find('span',class_='result-hood'))).group()
    price = clean_the_string(item.find('span',class_='result-price'))
    dist = clean_the_string(item.find('span',class_='maptag'))
    href = item.find('a',class_='result-image').attrs['href']

    if any([x not in hood.lower() for x in towns]) or hood == '':
        inDb = does_id_exist(pid)
        if not inDb:
            insert_into(pid)
            
        entry = {
            "title": name,
            "town": hood,
            "link": href,
            "price": price,
            "distance": dist,
            "isNew": not inDb
        }

        craig_entries.append(entry)

driver.quit()

airbnd_entries = airbnb.main()

send_email(craig_entries, airbnd_entries)


print('\nComplete\n')