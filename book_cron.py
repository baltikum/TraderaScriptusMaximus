    booking  = cron.new(command='/usr/bin/echo snopp',
                    comment=str(item_to_bid_on.objectNumber))
    booking.month.on(item_to_bid_on.end_month)
    booking.day.on(item_to_bid_on.end_day)
    booking.hour.on(item_to_bid_on.end_hour)
    booking.minute.on(item_to_bid_on.end_minute)
