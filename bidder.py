
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from crontab import CronTab
import time,traceback
import sys, os



base_url = 'https://www.tradera.com/'
item_base_url = base_url + 'item/'

def open_session():
    trace = ''
    try:
        #browser = webdriver.Firefox()
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        browser.get(base_url)
        time.sleep(1)

        xpath_accept_coockies = 'html/body/div[1]/div/div/div/div[2]/div/button[2]'
        button = browser.find_element(By.XPATH,xpath_accept_coockies)
        button.click()

        xpath_reject_all = (
            '/html/body/div[1]/div/div/div/div[1]/div/div[2]/button[1]')
        button = browser.find_element(By.XPATH,xpath_reject_all)
        button.click()

        xpath_save_reject = (
            '/html/body/div[1]/div/div/div/div[3]/div[2]/button')
        button = browser.find_element(By.XPATH,xpath_save_reject)
        button.click()

        time.sleep(1)
        res = True

    except:
        trace = traceback.format_exc()
        res = False
        browser = False

    return res, trace, browser

def tradera_login(driver,email,passw):
    trace = ''
    try:


        profile = driver.find_element(By.XPATH,"//*[@id='profile-button']")
        profile.click() 
        iframe = driver.find_element(By.XPATH,"//*[@id='sign-in-modal']")
        driver.switch_to.frame(iframe)      
        mail_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-mail']")
        passw_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-password']")
        login_button = driver.find_element(By.XPATH,"/html/body/div[1]/section/section/div/div[1]/div[1]/form/div[1]/div[2]/button")
        mail_input_field.send_keys(email)
        passw_input_field.send_keys(passw)
        login_button.click()
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res, trace


def main(argv):
    print('id: ' + argv[1])
    print('bid: ' + argv[2])

    email = os.environ['TRADERA_EMAIL']
    passw = os.environ['TRADERA_PASSW']

    res, trace, driver = open_session()
    if res:
        res, trace = tradera_login(driver,email,passw)
    else:
        print(trace)
    
    print(res)





if __name__ == '__main__' :
    main(sys.argv)
