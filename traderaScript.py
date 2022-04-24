
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import traceback, time, re, logging



email = ''
passw = ''
objectNumber = '536900083'



#Constants
OK = '##SUCCESS##'
FAIL = '##FAIL##'
BID_LIMIT = 500

#Webdriver
driver = False

#Driver fetched elements
mail_input_field = False
passw_input_field = False
login_button = False

#Status booleans
logged_in = False
driver_loaded = False
page_loaded = False
coockies_accepted = False
popup_opened = False
iframe_loaded = False
input_fields_fetched = False


class Item:
    def __init__(self,driver,objectNumber,bid,bid_limit):
        self.objectNumber = objectNumber
        self.driver = driver
        self.bid = bid
        self.bid_limit = bid_limit

        self.page_loaded = False

        self.bid_posted = False
        self.confirmed = False
        self.data_fetched = False


        self.bid_input_field = False
        self.bid_button = False
        self.confirm_bid_button = False


        self.title = ''
        self.price = ''
        self.ending = ''
        self.end_date_time = ''

    #Fetch basic info about object
    def fetch_item_data(self):
        trace = ''
        try:
            element = self.driver.find_element(By.XPATH,"//*[@id='view-item-main']")
            self.title = element.text
            element = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[1]/div[2]/p/span")
            self.price = element.text
            element = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[2]/p/span")
            self.ending = element.text
            element = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[1]/div[2]/div[1]/p")
            self.end_date_time = element.text
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Load object page into webdriver, returns true if successfull and trace
    def load_page(self):
        trace = ''
        try:
            self.driver.get(f"https://www.tradera.com/item/{self.objectNumber}")
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Find bidding elements
    def parse_bidding_elements(self):
        try:
            self.bidding_window = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[2]/form/div/input")
            self.bid_button = self.driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/div[1]/section[2]/form/button")
            res = True
        except:
            trace = traceback.format_exc()
            res = True
        return res, trace

    #Find confirm bid button, returns false or true if successful
    def parse_confirm_elements(self):
        try:
            self.confirm_bid_button = self.driver.find_element(By.XPATH,"/html/body/reach-portal/div[3]/div/div/div/div[2]/section/form/button")
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res

    #Post initial bid, returns false or true if succesful
    def post_bid(self):
        trace = ''
        try:
            self.bid_input_field.send_keys(self.bid)
            self.bid_button.click()
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Confirm the put bid, returns fale or true if succesful
    def confim_bid(self):
        trace = ''
        try:
            self.confirm_bid_button.click()
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace
    





#Check if valid object number
def check_valid_object_id(objectNumber):
    return ( int(objectNumber) and ( len(objectNumber) == 9 ) )

#Checks if the bid is an intger and between 0 and maximum limit
def check_valid_bid(bid):
    global BID_LIMIT
    trace = ''
    try:
        bid = int(bid)
        res = True
    except:
        trace = 'Bid not numeric'
        res = False

    if res:
        if bid > BID_LIMIT:
            trace = 'Bid above limit'
            res = False
        elif bid <= 0:
            trace = 'Bid 0 or negative'
            res = False

    return res, trace

#Check valid email
def check_valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

#Load webdriver
def load_webdriver():
    global driver
    res = False
    trace = ''
    try:
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Connect to page
def connect_to_page():
    global driver, maxattempts
    trace = ''
    try:
        driver.get("https://www.tradera.com/")
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Accept coockies
def accept_coockies():
    global driver
    trace = ''
    try:
        element = driver.find_element(By.XPATH,'html/body/div[1]/div/div/div/div[2]/div/button[2]')
        element.click()
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Open login popup window
def open_profile_popup():
    global driver
    trace = ''
    try:
        profile = driver.find_element(By.XPATH,"//*[@id='profile-button']")
        profile.click()
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Load login iframe
def load_popup_iframe():
    global driver
    trace = ''
    try:
        iframe = driver.find_element(By.XPATH,"//*[@id='sign-in-modal']")
        driver.switch_to.frame(iframe)
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Fetch login input fields
def fetch_input_fields():
    global driver,mail_input_field,passw_input_field,login_button
    trace = ''
    try:
        mail_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-mail']")
        passw_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-password']")
        login_button = driver.find_element(By.XPATH,"/html/body/div[1]/section/section/div/div[1]/div[1]/form/div[1]/div[2]/button")
        res = True
    except:
        trace = traceback.format_exc()
        res = False
    return res,trace

#Fill input fields and login
def post_login(email,passw):
    global driver,mail_input_field,passw_input_field,login_button
    trace = ''
    try:
        mail_input_field.send_keys(email)
        passw_input_field.send_keys(passw)
        login_button.click()
        res = True
    except:
        trace = traceback.format_exc()
        res = False

    return res, trace

def test_item(item):
    loaded,trace = item.load_page()
    if loaded:
        item.page_loaded = True

        fetched, trace = item.fetch_item_data()
        if fetched:
            print(f'{OK} Item data fetched.')
            item.data_fetched = True
            print(f'Title: {item.title}')
            print(f'Ending in: {item.ending}')
            print(f'At date time: {item.end_date_time}')
            print(f'Current price: {item.price}')

    return loaded and fetched, trace

def post_bid(item):
    res = False
    if login():
        success,trace1 = test_item(item)
        if success:
            parsed, trace2 = item.parse_bidding_elements()
            if parsed:
                item.bid_item_field.send_keys(item.bid)
                item.bid_button.click()
                parsed, trace3 = item.parse_confirm_elements()
                if parsed:
                    try:
                        item.confirm_bid_button.click()
                        res = True
                    except:
                        trace = traceback.format_exc()
                else:
                    trace = trace3
            else:
                trace= trace2
        else:
            trace = trace1
    return res, trace

def login():

    loaded, trace = load_webdriver()
    if loaded:
        driver_loaded = True
        print(f'{OK} Webdriver loaded.')
    else:
        print(trace)
        exit(f'{FAIL} WebDriver failed to load.')

    connection, trace = connect_to_page()
    if connection:
        page_loaded = True
        print(f'{OK} Page loaded.')
    else:
        print(trace)
        exit(f'{FAIL} Could not load the page.')

    time.sleep(2)
    coockies, trace = accept_coockies()
    if coockies:
        coockies_accepted = True
        print(f'{OK} Coockies accepted.')
    else:
        print(trace)
        exit(f'{FAIL} Could not accept coockies.')

    opened, trace = open_profile_popup()
    if opened:
        popup_opened = True
        print(f'{OK} Profile popup activated.')
    else:
        print(trace)
        exit(f'{FAIL} Cant find Login profile button.')

    loaded, trace = load_popup_iframe()
    if loaded:
        iframe_loaded = True
        print(f'{OK} Popup iframe loaded in driver.')
    else:
        print(trace)
        exit(f'{FAIL} Could not find popup login iframe.')

    fetched, trace = fetch_input_fields()
    if fetched:
        input_fields_fetched = True
        print(f'{OK} Login input fields found.')
    else:
        print(trace)
        exit(f'{FAIL} Could not find login input fields.')

    if (driver_loaded and page_loaded and coockies_accepted and 
            popup_opened and iframe_loaded and input_fields_fetched) :

            logged_in, trace = post_login(email,passw)
            if logged_in:
                print(f'{OK} Login successfull.')
            else:
                print(trace)
                exit(f'{FAIL} Could not log in.')
    return logged_in
    

if __name__ == "__main__":

 
    #Get user credentials and verify login
    email = input("Enter email:")
    passw = input("Enter password:")
    run_login = check_valid_email(email)
    if run_login:
        print(f'{OK}Attempting to login with {email}...')
        res = login()
        if res:
            print(f'{OK} Credentials verified.')



    #Get objectnumber and bid ammount
    objectNumber = input("Enter objectnumber:")
    bid = input("Enter bid ammount:")

    valid_obj_id = check_valid_object_id(objectNumber)
    valid_bid, trace = check_valid_bid(bid)
    #Test connection to item
    if valid_bid and valid_obj_id:
        item_to_bid_on = Item(driver,objectNumber,bid,BID_LIMIT)
        success, trace = test_item(item_to_bid_on)
        if success:
            print(f'{OK} Item added successfully.')
        else:
            print(trace)

    







