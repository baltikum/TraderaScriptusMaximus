
from datetime import datetime
from selenium.webdriver.common.by import By
import time
import sys, os
import logging
from session import open_session, tradera_login
from item_to_bid import Item
from item_to_bid import load_item


logging.basicConfig(filename=f'1_log.log')
logging.info('hej')