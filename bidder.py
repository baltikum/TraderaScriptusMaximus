
from datetime import datetime
from selenium.webdriver.common.by import By
import time
import sys, os
import logging
from session import open_session, tradera_login
from item_to_bid import Item
from item_to_bid import load_item
from booker import remove_booking


def main(argv):
    logging.basicConfig(filename=f'{argv[1]}_log.log')

    email = os.environ['TRADERA_EMAIL']
    passw = os.environ['TRADERA_PASSW']

    item = Item(argv[1], argv[2])


    logging.info(f'ID:{argv[1]} BID: {argv[2]}')
    logging.info(f'USER: {email}')

    session, trace, driver = open_session()

    if not session:
        logging.error(trace)
    else:
        logged_in,trace = tradera_login(driver,email,passw)
        if not logged_in:
            logging.error(trace)
        else:
            loaded, trace = load_item(driver,item)
            if not loaded:
                logging.error(trace)
            else:
                logging.info(f'LOADED: {item}')
                print(item)
                




    xpath_bid = ("/html/body/div[1]/div[2]/div[2]/div/div[4]"
    "/aside/div[1]/section[2]/form/button")
    bid = driver.find_element(By.XPATH, xpath_bid)
    bid.click()




    xpath_time = ( "/html/body/div[1]/div[2]/div[2]"
                "/div/div[4]/aside/div[1]/section[1]/div[2]/div[2]/p/span")

    end_time = driver.find_element(By.XPATH, xpath_time)
    lista = end_time .text.split()
    while len(lista) > 2 :
        end_time = driver.find_element(By.XPATH, xpath_time)
        lista = end_time.text.split()
        time.sleep(5)


    if len(lista) == 2:
        end_time = lista[0]

    #rutan
    xpath_bid_input = ("/html/body/reach-portal/div[3]/div/"
        "div/div/div[2]/section[4]/form/div/input")
    bid_input = driver.find_element(By.XPATH, xpath_bid_input)
    bid_input.send_keys(item.bid)


    def accuratecountdown(t,start,margin):
        while((datetime.now()-start).total_seconds() < (t-margin) ):
            print(f'{(datetime.now()-start).total_seconds()} is less than {t-margin}')
        return True



    accuratecountdown(float(end_time),datetime.now(),1.0)

    #skicka
    #xpath_bid_send = ( "/html/body/reach-portal/div[3]/div"
    #    "/div/div/div[2]/section[4]/form/button")
    #bid_send = driver.find_element(By.XPATH, xpath_bid_send)
    #bid_send.click()

    logging.info(f'BID NOW: {datetime.now()}')

    remove_booking(item.object_number)


if __name__ == '__main__' :
    main(sys.argv)
