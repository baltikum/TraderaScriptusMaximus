

class Item:
    def __init__(self,driver,object_number,bid,bid_limit):
        self.driver = driver
        self.object_number = object_number
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

        self.end_month = 0
        self.end_day = 0
        self.end_hour = 0
        self.end_minute = 0

    #Parse end date times
    def parse_end_date_time(self, end_date):
        def translate_month(month):
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

        temp = end_date.split()
        self.end_month = translate_month(temp[2].lower())
        self.end_day = temp[1]

        temp = temp[3].split(':')
        self.end_hour = temp[0]
        self.end_minute = temp[1]

    #Fetch basic info about object
    def fetch_item_data(self):
        trace = ''
        try:
            xpath_title = "//*[@id='view-item-main']"
            title = self.driver.find_element(By.XPATH, xpath_title)
            self.title = title.text

            xpath_price = "/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/" +
                            "div[1]/section[1]/div[1]/div[2]/p/span"
            price = self.driver.find_element(By.XPATH, xpath_price)
            self.price = price.text

            xpath_end_date = "/html/body/div[1]/div[2]/div[2]/div/div[4]/" +
                                "aside/div[1]/section[1]/div[2]/div[1]/p"
            end_date = self.driver.find_element(By.XPATH, xpath_end_date)
            self.parse_end_date_time(end_date.text)

            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Load object page into webdriver, returns true if successfull and trace
    def load_page(self):
        trace = ''
        try:
            item_base_url = "https://www.tradera.com/item/"
            self.driver.get(f"{item_base_url}{self.object_number}")
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

    #Find bidding elements
    def parse_bidding_elements(self):
        try:
            xpath = "/html/body/div[1]/div[2]/div[2]/div/div[4]/aside/"
            xpath_w = xpath + "div[1]/section[2]/form/div/input"
            self.bidding_window = self.driver.find_element(By.XPATH, xpath_w)
            xpath_b = xpath + "div[1]/section[2]/form/button"
            self.bid_button = self.driver.find_element(By.XPATH, xpath_b)
            res = True
        except:
            trace = traceback.format_exc()
            res = True
        return res, trace

    #Find confirm bid button, returns false or true if successful
    def parse_confirm_elements(self):
        try:
            xpath_confirm = "/html/body/reach-portal/div[3]/div/div/div/" +
                            "div[2]/section/form/button"
            self.confirm_bid = self.driver.find_element(By.XPATH, xpath_confirm)
            res = True
        except:
            trace = traceback.format_exc()
            res = False
        return res, trace

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

    def __repr__(self):
        return f'Bid {self.bid} on {self.title}' +
        f' at {self.end_hour}:{self.end_minute}'
         f' the {self.end_day}/{self.end_month}'
