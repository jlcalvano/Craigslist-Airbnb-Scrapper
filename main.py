from utils.db import insert_into, does_id_exist
from utils.email_sender import send_email
import config


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import date 

DRIVER_PATH = "driver\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_argument('log-level=3')
# chrome_options.headless = True # also works

driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=chrome_options)
driver.get('https://newjersey.craigslist.org/search/roo?bundleDuplicates=1&search_distance=10&postal=07444&max_price=900&availabilityMode=0')

soup = BeautifulSoup(driver.page_source,'html.parser')


def clean_the_string(element):
    if element:
        text = element.getText().strip().title()
        #text = re.sub(r'[^\w]', ' ', text)
    else:
        text = ''
    return text


f  = open("result.txt", "w+")
towns = config.towns
entries = []

for item in soup.select('#search-results li'):
    pid = item.attrs['data-pid']
    name = clean_the_string(item.find('h3'))
    hood = clean_the_string(item.find('span',class_='result-hood'))
    price = clean_the_string(item.find('span',class_='result-price'))
    dist = clean_the_string(item.find('span',class_='maptag'))
    href = item.find('a',class_='result-image').attrs['href']

    if any([x not in hood.lower() for x in towns]) or hood == '':
        inDb = does_id_exist(pid)

        f.write(name + ' - ')
        f.write(hood + ' - ')
        f.write(price + ' - ')
        f.write(dist + ' - ')
        f.write(href + ' - ')
        f.write(pid)
        f.write('\n')

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

        entries.append(entry)


    
f.close()

driver.quit()

send_email(entries)


print('\nComplete\n')