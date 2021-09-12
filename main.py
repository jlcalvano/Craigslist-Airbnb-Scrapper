from db import insert_into, does_id_exist

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
towns = ['wanaque','butler','kinnelon','pompton','riverdale']

for item in soup.select('#search-results li'):

    pid = item.attrs['data-pid']
    name = clean_the_string(item.find('h3'))
    hood = clean_the_string(item.find('span',class_='result-hood'))

    if any([x in  hood.lower() for x in towns]) or hood == '':
        f.write(name + ' - ')
        f.write(hood + ' - ')
        f.write(clean_the_string(item.find('span',class_='result-price'))+ ' - ')
        f.write(clean_the_string(item.find('span',class_='maptag'))+ ' - ')
        f.write(pid)
        f.write('\n')

        if does_id_exist(pid):
            print(f'{name}: is in the database')
        else:
            print(f'{name}: is new')
            insert_into(pid)


        


f.close()

driver.quit()


print('\nComplete\n')