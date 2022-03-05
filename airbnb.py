from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import re
import datetime
import time
import pandas as pd
from dateutil import relativedelta

DRIVER_PATH = "driver\chromedriver.exe"
ser = Service(DRIVER_PATH)

def clean_the_string(element):
    if element:
        text = element.getText().strip().title()
    else:
        text = ''
    return text

def get_airbnb_results(start_date, end_date):
    print("\nRunning Airbnb...\n")

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')


    driver = webdriver.Chrome(service=ser,options=chrome_options)

    url = f'https://www.airbnb.com/s/Butler--New-Jersey--United-States/homes?date_picker_type=calendar&query=Butler%2C%20New%20Jersey%2C%20United%20States&checkin={start_date}&checkout={end_date}&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=weekend_trip&price_max=1400&search_type=filter_change'

    driver.get(url)
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div/div/div/div/div[1]/div/div[1]/main/div[2]/div/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div[2]/div/meta[1]")))
    except:
        raise
    finally:
        time.sleep(3)
        print("Airbnb found")
        soup = BeautifulSoup(driver.page_source,'html.parser')
        print(len(driver.page_source))
        
    entries = []
    for item in soup.find_all("div", class_="_8ssblpx"):
            airbnb_entry = {
                "id":"",
                "title":"",
                "url":"",
                "price":"",
                "rating":"",
                "review":"",
                "real-price": False
            }
            try:
                airbnb_entry["id"]= re.search(r'\d+((.|,)\d+)?',item.find("meta", {"itemprop":"url"})['content']).group()
            except:
                print("ID : Not Found")

            try:
                 airbnb_entry["title"]= item.find("meta", {"itemprop":"name"})['content']
            except:
                print("Title : Not Found")

            try:
                 airbnb_entry["url"]= item.find("meta", {"itemprop":"url"})['content']
            except:
                print("URL : Not Found")
            
            # try:
                 # airbnb_entry["price"]= "$"+ re.search(r'\d+((.|,)\d+)?',item.find("span", class_="_tyxjp1").get_text()).group()
            # except:
                # print("Price : Not Found")

            try:
                rating = item.find("span",class_="rpz7y38 dir dir-ltr").get_text()
                airbnb_entry["rating"]= rating
            except:
                print("Rating : Not Found")

            try:
                airbnb_entry["review"]= re.search(r'\d+((.|,)\d+)?',item.find("span",class_="r1xr6rtg dir dir-ltr").get_text()).group()
            except:
                print("Review : Not Found")

            try:
                airbnb_entry["usedBefore"] = True if str(airbnb_entry["id"]) in ['50515640','50084451'] else False
            except:
                pass

            entries.append(airbnb_entry)
            airbnb_entry = {}

    return entries

def main():

    today = datetime.date.today()
    start_date = today + relativedelta.relativedelta(months=1, day=1)
    end_date =  start_date + relativedelta.relativedelta(months=1)

    start_date = start_date.isoformat()
    end_date = end_date.isoformat()

    results = []
    attempts = 0
    while len(results) == 0 and attempts < 3:
        try: 
            attempts = attempts + 1
            results = get_airbnb_results(start_date, end_date)
        except:
            pass
    
    
    if results:
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(service=ser,options=chrome_options)
    
    for item in results:
   
        driver.get("https://" + item["url"])
        item["town"] = ""
        try:
            WebDriverWait(driver, 20).until(
               EC.element_to_be_clickable((By.CLASS_NAME, '_lwijk8d'))
            )
            WebDriverWait(driver, 20).until(
               EC.visibility_of_element_located((By.CLASS_NAME, '_1k4xcdh'))
            )
            WebDriverWait(driver, 20).until(
               EC.visibility_of_element_located((By.CLASS_NAME, '_8vvkqm3'))
            )
        except:
            print("exception")
            continue
        finally:
            print("listing page found")
            soup = BeautifulSoup(driver.page_source,'html.parser')
            
        item["town"] = clean_the_string(soup.find('span',class_="_8vvkqm3")).strip().split(",")[0]
        item["price"] = clean_the_string(soup.find('span',class_="_1k4xcdh")).strip()
        item["real-price"] = True


    print()
    print(f"Length of Results: {len(results)}")
    print()
    print(f"Number of Attempts: {attempts}")
    print()
    return results

if __name__ == '__main__':
    main()