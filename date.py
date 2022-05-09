
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from crontab import CronTab
import time,traceback

def switch(month):
    switch={
       'januari': 1,
       'februari': 2,
       'mars': 3,
       'april': 4,
       'maj': 5,
       'juni': 6,
       'juli': 7,
       'augusti': 8,
       'september':9,
       'oktober':10,
       'november':11,
       'december':12
       }
    return switch.get(month,0)

try:
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    #browser = webdriver.Firefox()
    browser.get('https://www.tradera.com/item/540763839')
    time.sleep(1)

    element = browser.find_element(By.XPATH,'html/body/div[1]/div/div/div/div[2]/div/button[2]')

    element.click()

    time.sleep(1)


    element = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[1]/p")
    temp = element.text
    temp = temp.split()

    print(f'date is {temp[1]}')
    print(f'month is {switch(temp[2].lower())}')

    temp = temp[3].split(':')
    print(f'hour is {temp[0]}')
    print(f'minute is {temp[1]}')

    booking  = cron.new(command='/usr/bin/echo snopp',
                    comment=str(item_to_bid_on.objectNumber))
    booking.month.on(item_to_bid_on.month)
    booking.day.on(item_to_bid_on.day)
    booking.hour.on(item_to_bid_on.hour)
    booking.minute.on(item_to_bid_on.minute)

except:
    traceback.print_exc()


browser.close()
