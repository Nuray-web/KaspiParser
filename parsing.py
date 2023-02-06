from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import xlsxwriter
import re
from selenium.webdriver.common.action_chains import ActionChains

rows = []
url = "https://kaspi.kz/shop/c/irons/?q=%3Acategory%3AIrons%3AmanufacturerName%3ARowenta%3AmanufacturerName%3ATefal%3AavailableInZones%3AMagnum_ZONE1&sort=relevance?page="


driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')
driver.maximize_window()
    
driver.get(url)
button = driver.find_element(By.XPATH, '//*[@id="dialogService"]/div/div[1]/div[1]/div/ul[1]/li[10]/a')
button.click()
    
soup = BeautifulSoup(driver.page_source)
    
while True:
    prev_url = driver.current_url
    soup = BeautifulSoup(driver.page_source)
    products = soup.find_all('div', class_='item-card ddl_product ddl_product_link undefined')

    for i in products:
        title = i.find('a', class_='item-card__name-link').text.strip()
        brand = title.split(' ')[0]
        link = i.a.get('href')
        price = i.find('span', class_='item-card__prices-price').text.strip().replace('₸', '').replace(u'\xa0', '')
        print(brand, title.replace(brand,''), link)
        info = {'Brand': brand,
                'Title': title.replace(brand,''),
                'Price': price,
                'Link': link}
        driver.get(link)
    
        insoup = BeautifulSoup(driver.page_source)
        driver.execute_script("window.scrollBy(0, 1500);")
        driver.implicitly_wait(20)
        time.sleep(10)
        sellers = insoup.find_all('tr')
        
        sells = []
        for i in sellers:
            try:
                d = {}
                seller = i.find('td', class_='sellers-table__cell').text.strip()
                seller = re.sub("\(.*?\)", '', seller)
                sellprice = i.find('div', class_='sellers-table__price-cell-text').text.strip().replace('₸', '').replace(u'\xa0', '')
                print(seller, sellprice)
                d['Seller'] = seller
                d['SellerPrice'] = sellprice
            except:
                pass
            sells.append(d)
        
        for i in sells:
            new_info = info.copy()
            new_info.update(i)
            rows.append(new_info)
    driver.get(prev_url)
    driver.find_element(By.CLASS_NAME, 'pagination').find_elements(By.TAG_NAME, 'li')[-1].click()
    time.sleep(4)
    print(driver.current_url)
    if prev_url == driver.current_url:
        break
        

  
