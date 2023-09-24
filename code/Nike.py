from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import ssl
from urllib.request import urlopen
from selenium import webdriver
from urllib.error import URLError, HTTPError
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

subprocess.Popen(r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

# 나이키 홈페이지 우회

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)

# 런닝 카테고리 나이키 홈페이지 접속

url='https://www.nike.com/kr/ko_kr/w/new/fw/xc/new-mens-shoes?productSports=02'

driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #스크롤 내리기
driver.find_element_by_xpath('//*[@id="load-more"]').click()  #더보기 클릭
driver.execute_script("window.scrollTo(0,0)")           # 스크롤 다시 올리기

name_list = []   #상품이름
ex_list = []     #상품설명
code_list = []   #상품코드

for i in range(1,53):
    try:
           driver.find_element_by_xpath('/html/body/section/section/section/article/div/div[2]/ul/li[%s]/div/div[1]/a/span'%i).click()
           time.sleep(10)
           html = driver.page_source
           soup = BeautifulSoup(html, 'html.parser')
           img = soup.find('div',{'class':'prd-gutter'})  #img url 
           img2 = img.find('img')['src']
           img3 = soup.find_all('div',{'class':'prd-gutter'})  #신발 밑창img url
           img4 = img3[1]
           img5 = img4.find('img')['src']
           driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)  # 더보기 칸을 보기 위해 한칸 내리도록 함
           code = soup.find('span',{'class':'style-code'}).text                # 더보기 클릭 전 상품번호 크로링
           code = code.split(":")[1].replace(" ","")
           code_list.append(code)

           driver.find_element_by_xpath('/html/body/section/section/section/article/article[2]/div/div[4]/div/div[5]/div[1]/a').send_keys(Keys.ENTER)
        
           html = driver.page_source
           soup = BeautifulSoup(html, 'html.parser')

           name = soup.find('span',{'class':'tit'}).text                   #상품 이름 크롤링
           name_list.append(name)
            
           ex = soup.find('div',{'class':'pdp-description-preview'}).text   #상품 설명 크콜링
           ex_list.append(ex)

           with urlopen(img2) as f:                                          # 이미지파일 이름에 코드번호가 나올 수 있도록 하기 위해 code 번호가 크롤링된 후 이미지 저장
               with open('런닝/'+code+'.jpg','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
                   img = f.read() #이미지 읽기
                   h.write(img) # 이미지 저장

           with urlopen(img5) as f:                                            #신발 밑창 사진
               with open('런닝/'+code+'2.jpg','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
                   img = f.read() #이미지 읽기
                   h.write(img) # 이미지 저장

           time.sleep(4)
           driver.get(url)
            
           print(i,"번째 "+name+" 상품 크롤링이 완료 되었습니다.")


    except NoSuchElementException as n :
            try:

                driver.find_element_by_xpath('/html/body/section/section/section/article/article[2]/div/div[4]/div/div[4]/div[1]/a').send_keys(Keys.ENTER)
        
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
            
                name = soup.find('span',{'class':'tit'}).text
                name_list.append(name)
            
                ex = soup.find('div',{'class':'pdp-description-preview'}).text
                ex_list.append(ex)

                with urlopen(img2) as f:                                          # 이미지파일 이름에 코드번호가 나올 수 있도록 하기 위해 code 번호가 크롤링된 후 이미지 저장
                    with open('런닝/'+code+'.jpg','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
                        img = f.read() #이미지 읽기
                        h.write(img) # 이미지 저장

                with urlopen(img5) as f:                                            #신발 밑창 사진
                    with open('런닝/'+code+'2.jpg','wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
                        img = f.read() #이미지 읽기
                        h.write(img) # 이미지 저장
            
        
                time.sleep(4)
                driver.get(url)
                print(i,"번째 "+name+" 상품 크롤링이 완료 되었습니다.")
            except NoSuchElementException as n :
                print('광고 배너입니다.')
                pass
                

df = pd.DataFrame([name_list,code_list,ex_list]).T    # 데이터 프레임 생성
df.columns=['상품명','상품 코드','상세 설명']           #컬럼 생성
