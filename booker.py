
from datetime import datetime
from item_to_bid import Item
from crontab import CronTab
import sys

def remove_booking(id):
    cron = CronTab(user=True)
    available = cron.find_comment(comment=str(id))
    if available:
        cron.remove_all(comment=str(id))
    return 

def add_booking(id, bid):
    item = Item(id, bid)

    cron = CronTab(user=True)

    full_bidder_path = 'home/baltikum/Documents/TraderaScriptusMaximus/bidder.py'
    job = cron.new(command=f'/usr/bin/python3 {full_bidder_path} {item.object_number} {item.bid}'
                , comment=f'{item.object_number} {datetime.now()}')

    job.hour.on(int(item.end_hour))
    job.minute.on((int(item.end_minute) - 2))
    job.day.on(int(item.end_day))
    job.month.on(int(item.end_month))
    job.enable()
    cron.write()

    return


if __name__ == '__main__' :
    add_booking(sys.argv[1],sys.argv[2])
