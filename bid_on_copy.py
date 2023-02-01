


from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, sys 

#start = time.time()

#from pyvirtualdisplay import Display
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#display = Display(visible=0, size=(800, 600))
#display.start()
#browser = webdriver.Chrome()


login_url = "https://www.tradera.com/login?returnUrl=%2F&login-modal=true"
url = "https://www.tradera.com/item/"
itemNumber = sys.argv[1]
maxBid = sys.argv[2]
itemUrl = url + str(itemNumber)


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

#BIDDING
browser.get(itemUrl)
bid_button = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[2]/form/button")
bid_button.click()

#GET TIME
ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
split_time_parts = ends_in.text.split()

#LOOP TIL SECONDS
while len(split_time_parts) > 2:
    time.sleep(5)
    ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
    split_time_parts = ends_in.text.split()

#LOOP TIL LAST SECONDS
while int(split_time_parts[0]) > 6:
    time.sleep(1)


#LOAD ELEMENTS AND FILL BID
field = "/html/body/reach-portal/div[2]/div/div/div/div[2]/section[4]/form/div/input"
but = "/html/body/reach-portal/div[2]/div/div/div/div[2]/section[4]/form/button"
bid_field = browser.find_element(By.XPATH,field)
bid_button = browser.find_element(By.XPATH,but)
bid_field.send_keys(str(maxBid))

#FINAL LOOP COUNTDOWN
while int(split_time_parts[2]) > 2:
    time.sleep(0.2)
    ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
    split_time_parts = ends_in.text.split()

bid_button.click()
print(split_time_parts[2])
    


