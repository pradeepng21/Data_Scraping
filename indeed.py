from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
import re
import requests
from pymongo import MongoClient
op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging'])
ser = Service("C:\\Users\\Pradeep_NG\\Desktop\\chromedriver_win32\\chromedriver.exe")
browser = webdriver.Chrome(service=ser, options=op)
connection_string = "mongodb://localhost:27017"
client = MongoClient(connection_string)
print(client.list_database_names())

for a in range(2):

    jobs=['python','machine learning']
    browser.get("https://www.naukri.com")
    sleep(1)
    search = browser.find_element(By.CLASS_NAME, 'suggestor-input')
    search_button = browser.find_element(By.CLASS_NAME, 'qsbSubmit')
    search.send_keys(jobs[a])
    sleep(2)
    search_button.click()
    sleep(3)
    li=[]
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sleep(1)
    ti = []
    for i in soup.find_all('a', class_='title fw500 ellipsis'):
        ti.append(i.get('href'))
    print(ti)            
    k = len(ti)
    for i in range(k):
        browser.get(ti[i])
        browser.implicitly_wait(10)
        dict={}
        try:
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find_all('h1', class_='jd-header-title')
            dict['title'] = [title[0].text]
            comp_name = soup.find_all('a', class_ = 'pad-rt-8')
            dict['company_name'] = [comp_name[0].text]
            rating = soup.find_all('span', class_= 'amb-rating pad-rt-4')
            try:
                dict['rating'] = [rating[0].text]
            except:
                dict['rating'] = 'null'
            exp = soup.find_all('div', class_='exp')
            try:
                dict['experience'] = [exp[0].text]
            except:
                dict['experience'] = 'null'
            sal = soup.find_all('div', class_='salary')
            try:
                dict['sal'] = [sal[0].text]
            except:
                dict['sal'] = 'null'    
            loc = soup.find_all('div', class_='loc')#can be stored only in dictionaries
            dict['loc'] = [j.text for j in loc]
            desc = soup.find_all('div', class_='dang-inner-html')
            dict['desc'] = [desc[0].text]
            dict['about_company'] = [desc[1].text]
            role = soup.find_all('div', class_='details')
            dict['role'] = [role[0].text]
            dict['ind_type'] = [role[1].text]
            dict['emp_type'] = [role[3].text]
            edu = soup.find_all('div', class_='education')
            dict['education'] = [j.text for j in edu]
            skills = soup.find_all('div', class_='key-skill')
            dict['skills'] = [j.text for j in skills]
            
        except:
            dict['about_company'] = 'null'

db = client['Job']
mydb=db['data']

y=mydb.insert_many(dict)