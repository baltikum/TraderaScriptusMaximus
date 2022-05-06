from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
import time


browser = webdriver.Firefox()
browser.get('https://www.tradera.com/item/290923/538733449/voice-patrol-tactical-commander-figur-')

element = browser.find_element(By.XPATH,'html/body/div[1]/div/div/div/div[2]/div/button[2]')
element.click()

time.sleep(2)
now = datetime.now()
first = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[2]/p/span")
now2 = datetime.now()


lista = first.text.split()

if len(lista) == 2:
    index = 0
else:
    index = 2

first = lista[index]


margin = (now2-now).total_seconds()


second = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[2]/p/span").text.split()[index]

while (first == second):
    time.sleep(0.1)
    second = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[2]/p/span").text.split()[index]
    
print(margin)


def accuratecountdown(t,start,margin):
    while((datetime.now()-start).total_seconds() < (t-margin) ):
        print(f'{(datetime.now()-start).total_seconds()} is less than {t-margin}')
    return True



accuratecountdown(float(second),datetime.now(),margin)


now3 = datetime.now()
second = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[2]/button/span[1]").text

now4 = datetime.now()


print(f'{(now4-now3).total_seconds()} is the time to fetch {second}')


browser.close()













