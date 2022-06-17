
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import traceback, time, re, logging, os, json
import configparser

from crontab import CronTab
from item_to_bid import Item

class Tradera():
    def __init__(self, BID_LIMIT):
    #Constants
        self.OK = '##SUCCESS##'
        self.FAIL = '##FAIL##'
        self.BID_LIMIT = BID_LIMIT
    #WebDriver
        self.driver = False
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--window-size=1920,1200")

    #Driver fetched elements
        self.mail_input_field = False
        self.passw_input_field = False
        self.login_button = False

    #Status booleans
        self.logged_in = False
        self.driver_loaded = False
        self.page_loaded = False
        self.coockies_accepted = False
        self.popup_opened = False
        self.iframe_loaded = False
        self.input_fields_fetched = False




    #Check if valid object number
    def check_valid_object_id(objectNumber):
        return ( int(objectNumber) and ( len(objectNumber) == 9 ) )

    #Checks if the bid is an intger and between 0 and maximum limit
    def check_valid_bid(self, bid):
        trace = ''
        try:
            bid = int(bid)
            res = True
        except:
            trace = 'Bid not numeric'
            res = False

        if res:
            if bid > self.BID_LIMIT:
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
    def load_webdriver(self):

 

        res = False
        trace = ''
        try:
            self.driver = webdriver.Firefox(options=self.options,executable_path=GeckoDriverManager().install())
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Connect to page
    def connect_to_page(self, url):
        trace = ''
        try:
            self.driver.get(url)
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Accept coockies
    def accept_coockies(self):
        trace = ''
        try:
            coockies_xpath = 'html/body/div[1]/div/div/div/div[2]/div/button[2]'
            element = self.driver.find_element(By.XPATH,coockies_xpath)
            element.click()
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Open login popup window
    def open_profile_popup(self):
        trace = ''
        try:
            profile = self.driver.find_element(By.XPATH,"//*[@id='profile-button']")
            profile.click()
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Load login iframe
    def load_popup_iframe(self):
        trace = ''
        try:
            iframe = self.driver.find_element(By.XPATH,"//*[@id='sign-in-modal']")
            self.driver.switch_to.frame(iframe)
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Fetch login input fields
    def fetch_input_fields(self):
        trace = ''
        try:
            self.mail_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-mail']")
            self.passw_input_field = driver.find_element(By.XPATH,"//*[@id='login-box-password']")
            self.login_button = driver.find_element(By.XPATH,"/html/body/div[1]/section/section/div/div[1]/div[1]/form/div[1]/div[2]/button")
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res,trace

    #Fill input fields and login
    def post_login(self, email, passw):
        trace = ''
        try:
            self.mail_input_field.send_keys(email)
            self.passw_input_field.send_keys(passw)
            res = self.login_button.click()
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    def test_item(self, item):
        loaded,trace = self.connect_to_page(self, item.url)
        if loaded:
            item.page_loaded = True

            fetched, trace = item.fetch_item_data()
            if fetched:
                print(f'{self.OK} Item data fetched.')
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

    def login(email, passw):

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
                    #exit(f'{FAIL} Could not log in.')
        return logged_in

    def load_user():
        try:
            config_file = configparser.ConfigParser()
            config_file.read("configurations.ini")
            email = config_file["TraderaUserCredentials"]["username"]
            passw = config_file["TraderaUserCredentials"]["password"]
            res = True
        except:
            email = ''
            passw = ''
            res = False
        return res, email, passw

    def write_user_to_config(email,passw):
        trace = ''
        try:
            config_file = configparser.ConfigParser()
            config_file.add_section("TraderaUserCredentials")
            config_file.set("TraderaBidderSettings", "username", email )
            config_file.set("TraderaBidderSettings", "password", passw )
            with open(r"configurations.ini", 'w') as file:
                config_file.write(file)
                file.flush()
                file.close()
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    def write_booking_file(item):
        data = []
        data.append('{ title: ')
        data.append(str(item.title))
        data.append(", object_number: ")
        data.append(str(item.objectNumber))
        data.append(", bid_ammount: ")
        data.append(str(item.bid))
        data.append(", end_month: ")
        data.append(str(item.end_month))
        data.append(", end_day: ")
        data.append(str(item.end_day))
        data.append(", end_hour: ")
        data.append(str(item.end_hour))
        data.append(", end_minute: ")
        data.append(str(item.end_minute))
        data.append("}")
        data = ''.join(data)
        data = json.dumps(data)

        with open( (str(item.objectNumber) + '.txt') , 'rw') as file:
            res = file.write(data)
        return res

if __name__ == "__main__":

    email = os.environ['TRADERA_EMAIL']
    passw = os.environ['TRADERA_PASSW']
    
    print(f'{OK}Attempting to login with {email}...')
    res = login(email,passw)
    if res:
        print(f'{OK} Credentials verified.')

    res = driver.get('https://www.tradera.com/my/saved-searches')
   
    print(driver.page_source)

    e = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/section[2]/section/form/section[3]/div[2]')
    print(e.get_text)

    print(driver.title)
    print(driver.current_url) 


'''
    #Get objectnumber and bid ammount
    objectNumber = input("Enter objectnumber:")
    bid = input("Enter bid ammount:")

    valid_obj_id = check_valid_object_id(objectNumber)
    valid_bid, trace = check_valid_bid(bid)
    #Test connection to item
    if valid_bid and valid_obj_id:
        item_to_bid_on = Item(driver,objectNumber,bid,BID_LIMIT)
        success, trace = test_item(item_to_bid_on)
        print(f'You want to bid {bid} on {objectNumber}')
        res = write_booking_file(item_to_bid_on)
        if success and res :
            cron = CronTab(user='baltikum')
            dir = os.getcwd()
            print(dir)
            booking  = cron.new(command='/usr/bin/echo snopp',
                            comment=str(item_to_bid_on.objectNumber))
            booking.month.on(item_to_bid_on.end_month)
            booking.day.on(item_to_bid_on.end_day)
            booking.hour.on(item_to_bid_on.end_hour)
            booking.minute.on(item_to_bid_on.end_minute)
            cron.write()

            #job = cron.new(command="DISPLAY=:0 /usr/bin/python3 "
            #                + "/home/baltikum/Documents/TraderaScriptusMaximus/bidding.py"
            #                + " > /home/baltikum/Documents/TraderaScriptusMaximus/skript_log.txt" )
            #cron.write()
            print(f'{OK} Item added successfully.')
        else:
            print(trace)'''
