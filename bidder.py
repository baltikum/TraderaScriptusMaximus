
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from crontab import CronTab
import time,traceback



base_url = 'https://www.tradera.com/'
item_base_url = base_url + 'item/'
def bid_session(item):
    try:
        #browser = webdriver.Firefox()
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        browser.get(base_url)
        time.sleep(1)

        xpath_accept_coockies = 'html/body/div[1]/div/div/div/div[2]/div/button[2]'
        button = browser.find_element(By.XPATH,xpath_accept_coockies)
        button.click()

        time.sleep(1)




    except:
        traceback.format_exc()


    browser.close()

if __main__ ==
