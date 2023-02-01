from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, traceback,sys 

from multiprocessing import Process,Pipe,Queue


def BIDDERPROCESS(QUE_OUT,QUE_IN):
    login_url = "https://www.tradera.com/login?returnUrl=%2F&login-modal=true"
    url = "https://www.tradera.com/item/"

    #DRIVER
    options = webdriver.FirefoxOptions()      
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
    browser.get(login_url)
    time.sleep(3)


    #ACCEPT COOCKIES
    xpath_accept_coockies = 'html/body/div[1]/div/div/div/div[2]/div/button[2]'
    button = browser.find_element(By.XPATH,xpath_accept_coockies)
    button.click()

    #LOGIN
    uname = browser.find_element(By.XPATH,"//*[@id=\"login-box-mail\"]")
    passw = browser.find_element(By.XPATH,"//*[@id=\"login-box-password\"]")
    uname.send_keys("mwdavidsson@outlook.com")
    passw.send_keys("Elwyn2021?!")
    login_button = browser.find_element(By.XPATH,"/html/body/div[1]/section/section/div/div[1]/div[1]/form/div[1]/div[2]/button")
    login_button.click()
    
    msg = {"STATUS": "READY"}
    QUE_OUT.put(msg)
    

    while True:
        time.sleep(2)
        if not QUE_IN.empty():
            item = QUE_IN.get()
            print(item)
            break

 
    browser.get(url + str(item['itemNumber']))

       
