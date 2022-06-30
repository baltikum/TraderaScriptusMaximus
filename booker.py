from item_to_bid import Item
from crontab import CronTab
import sys

from session import open_session
from selenium.webdriver.common.by import By




def remove_booking(id):
    cron = CronTab(user=True)
    available = cron.find_comment(comment=str(id))
    if available:
        cron.remove_all(comment=str(id))
        cron.write()
        return True
    return False

def add_booking(id, bid):
    item = Item(id, bid)
    res,trace, browser = open_session()
    if res:
        item.load_item(browser)
    else:
        print(trace)
        return False

    cron = CronTab(user=True)

    full_bidder_path = '~/Dokument/TraderaScriptusMaximus/bidder.py'
    job = cron.new(command=f'/usr/bin/python3 {full_bidder_path} {item.object_number} {item.bid}'
                , comment=f'{item.object_number}')

    job.hour.on(int(item.end_hour))
    job.minute.on((int(item.end_minute) - 2))
    job.day.on(int(item.end_day))
    job.month.on(int(item.end_month))
    job.enable()
    cron.write()

    return True


if __name__ == '__main__' :
    if len(sys.argv) == 3:
        ret = add_booking(sys.argv[1],sys.argv[2])
        print('Added.')
    elif len(sys.argv) == 2:
        ret = remove_booking(sys.argv[1])
        if ret:
            print('Removed')
        else:
            print('Not removed')
    else:
        print('Parameter error.')
