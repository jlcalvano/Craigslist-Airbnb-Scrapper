from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

DRIVER_PATH = "driver\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works

driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=chrome_options)
driver.get('https://newjersey.craigslist.org/search/roo?bundleDuplicates=1&search_distance=10&postal=07444&availabilityMode=0')

soup = BeautifulSoup(driver.page_source,'html.parser')


def clean_the_string(element):
    if element:
        text = element.getText().strip().title()
        #text = re.sub(r'[^\w]', ' ', text)
    else:
        text = ''
    return text


f  = open("result.txt", "w+")


for item in soup.select('#search-results li'):

    print('')
    print(clean_the_string(item.find('h3')))
    print(clean_the_string(item.find('span',class_='result-hood')))
    print(clean_the_string(item.find('span',class_='result-price')))
    print(clean_the_string(item.find('span',class_='maptag')))
    print(item.attrs['data-pid'])

    
    f.write(clean_the_string(item.find('h3')) + ' - ')
    f.write(clean_the_string(item.find('span',class_='result-hood'))+ ' - ')
    f.write(clean_the_string(item.find('span',class_='result-price'))+ ' - ')
    f.write(clean_the_string(item.find('span',class_='maptag'))+ ' - ')
    f.write(item.attrs['data-pid'])
    f.write('\n')


f.close()

driver.quit()