
import traceback
from selenium.webdriver.common.by import By


class Item:
    def __init__(self,object_number,bid):
        self.object_number = object_number
        self.bid = bid
        self.URL = "https://www.tradera.com/item/" + str(object_number)

        #interface
        self.page_loaded = False
        self.bid_posted = False
        self.confirmed = False
        self.data_fetched = False
        self.bid_input_field = False
        self.bid_button = False
        self.confirm_bid_button = False

        #Item info
        self.title = ''
        self.price = ''

        #parsed date
        self.end_month = 0
        self.end_day = 0
        self.end_hour = 0
        self.end_minute = 0



    def load_item(self,driver):
        driver.get(self.URL)
        loaded, trace = self.query_item(driver)
        return loaded, trace

    def query_item(self,driver):
        res, trace = self.fetch_item_data(driver)
        return res, trace
        
    def post_bid_ext(self, driver, bid):

        res, trace = self.fetch_item_data(self, driver)
        if not res:
            return res, trace

        

        res, trace = self.parse_bidding_elements(self, driver)
        if not res:
            return res, trace

        res, trace = self.int_post_bid(self, driver)
        if not res:
            return res, trace

        res, trace = self.parse_confirm_elements(self, driver)
        if not res:
            return res, trace
        

        #Countdown

        res, trace = self.confim_bid(self)

        return res, trace

    #Parse end date times
    def parse_end_date_time(self, end_date):
        def translate_month(month):
            switch={
               'jan': 1,
               'feb': 2,
               'mar': 3,
               'aprl': 4,
               'maj': 5, #
               'jun': 6, #confirmed
               'jul': 7,
               'aug': 8,
               'sep':9,
               'okt':10,
               'nov':11,
               'dec':12
               }
            return switch.get(month,0)

        temp = end_date.split()
        self.end_month = translate_month(temp[2].lower())
        self.end_day = temp[1]

        temp = temp[3].split(':')
        self.end_hour = temp[0]
        self.end_minute = temp[1]

    #Fetch basic info about object
    def fetch_item_data(self,driver):
        trace = ''
        try:
            xpath_title = "//*[@id='view-item-main']"
            title = driver.find_element(By.XPATH, xpath_title)
            self.title = title.text

            xpath_price = ("/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/" +
                            "div[1]/section[1]/div[1]/div[2]/p/span")
            price = driver.find_element(By.XPATH, xpath_price)
            self.price = price.text

            xpath_end_date = ("/html/body/div[1]/div[2]/div[2]/div/div[4]/" +
                                "aside/div[1]/section[1]/div[2]/div[1]/p")
            end_date = driver.find_element(By.XPATH, xpath_end_date)
            self.parse_end_date_time(end_date.text)

            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Find bidding elements
    def parse_bidding_elements(self, driver):
        try:
            xpath = "/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/"
            xpath_w = xpath + "div[1]/section[2]/form/div/input"
            self.bidding_window = driver.find_element(By.XPATH, xpath_w)
            xpath_b = xpath + "div[1]/section[2]/form/button"
            self.bid_button = driver.find_element(By.XPATH, xpath_b)
            res = True
        except:
            trace = traceback.format_exc()
            res = True
        return res, trace

    #Find confirm bid button, returns false or true if successful
    def parse_confirm_elements(self, driver):
        try:
            xpath_confirm = ("/html/body/reach-portal/div[3]/div/div/div/" +
                            "div[2]/section/form/button")
            self.confirm_bid = driver.find_element(By.XPATH, xpath_confirm)
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Post initial bid, returns false or true if succesful
    def int_post_bid(self):
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

    def __repr__(self):
        return (
            f'Bid {self.bid}kr on : \n{self.title}\n' +
            f'At {self.end_hour}:{self.end_minute}' +
            f'the {self.end_day}/{self.end_month}.\n' +
            f'Price currently at {self.price}.' )
