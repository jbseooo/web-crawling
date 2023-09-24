from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.chrome.options import Options
import os, shutil
import pandas as pd
from urllib.request import urlopen

import time
import random

### 조던 나이키 url https://cafe.naver.com/sssw?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625158%26search.menuid=394%26search.boardtype=L%26search.totalCount=151%26search.cafeId=10625158%26search.page={}

### 이지 아디다스 url https://cafe.naver.com/sssw?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625158%26search.menuid=427%26search.boardtype=L%26search.totalCount=151%26search.cafeId=10625158%26search.page=1

## 슈프림   https://cafe.naver.com/sssw?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625158%26search.menuid=423%26search.boardtype=L%26search.totalCount=151%26search.cafeId=10625158%26search.page=1

## 뉴발란스 https://cafe.naver.com/sssw?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625158%26search.menuid=484%26search.boardtype=L%26search.totalCount=151%26search.cafeId=10625158%26search.page=1

d =[]
date_list =[]
chromedriver_path = '/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options = options)

for i in range(1,100):
    print(i)
    url = 'https://cafe.naver.com/sssw?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625158%26search.menuid=423%26search.boardtype=L%26search.totalCount=151%26search.cafeId=10625158%26search.page={}'.format(i)
    driver.get(url)
    driver.switch_to.frame('cafe_main')
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    date = soup.find_all('td',{'class':'td_date'})
    for k in date:
        k2 = k.get_text()
        date_list.append(k2)
    
    
    con = soup.find_all('a',{'class':'article'})
    for z in con:
        c = z.get_text()
        result2 = c.lstrip()
        result2 = result2.rstrip()
        d.append(result2)
        
    
    time.sleep( random.uniform(2,4))

df = pd.DataFrame(date_list)
df['2'] = d
df.to_excel('data.xlsx')
