


from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, traceback,sys, json



start = time.time()



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



####### OPEN BROWSER DRIVER AND LOGIN #######
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



empty_item_file = """{
  "to_bid_on": []
}"""


bid_on = {}
temp_file = []

while True:



    while True:
        try:
            with open('bid_on_theese.txt','rw') as file:
                temp_file = file.readlines()
            break
        except IOError:
            time.sleep(3)


    temp = ""
    for entry in temp_file:
        temp.join(entry)

    if len(temp) > 0:
        items = json.loads(temp)

    if len(items) > 0:
        item_list = items['to_bid_on']
        for item in item_list:
            if item['action'] == "BID":
                bid_on[item['id']] = item
            elif item['action'] == "REMOVE":
                bid_on.pop(item['id'])
            elif item['action'] == "UPDATE":
                bid_on[item['id']] = item
            else:
                print("ERROR")



    else:
        time.sleep(300)


"""

{
  "to_bid_on": [
    {
      "id": "12345678",
      "bid": "100",
      "action": "BID",
      "at_time": "DÅ"
    },
    {
      "id": "12345678",
      "bid": "100",
      "action": "BID",
      "at_time": "DÅ"
    }
  ]
}

"""


####### BID ON SPECIFIC ITEM #######

#BIDDING
browser.get(url + str(itemNumber))
bid_button = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[2]/form/button")
bid_button.click()
#Wait for last  60 seconds
ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
split_time_parts = ends_in.text.split()
while len(split_time_parts) > 2:
    time.sleep(10)
    ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
    split_time_parts = ends_in.text.split()

#Wait for the last 6 seconds
while int(split_time_parts[0]) > 6:
    time.sleep(2)
    ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
    split_time_parts = ends_in.text.split()

ends_in = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[1]/div[2]/div[2]/p/span")
split_time_parts = ends_in.text.split()

#Fill bid input
confirm_input = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section/form/div/input")
confirm_input.send_keys(maxBid)

#wait for lastsecond
while int(split_time_parts[0]) > 2:
    time.sleep(0.2)
#BID
confirm_bid_button = browser.find_element(By.XPATH,"/html/body/reach-portal/div[2]/div/div/div/div[2]/section[4]/form/button")
confirm_bid_button.click()



