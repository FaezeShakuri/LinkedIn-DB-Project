# $ pip install schedule

import schedule
import time
import datetime
import server

def birthday_notifications():
    day = datetime.datetime.today().day
    month = datetime.datetime.today().month
    server.create_birthday_notifications(day, month)

schedule.every().day.at("03:30").do(birthday_notifications)

while True:
    schedule.run_pending()
    time.sleep(1)
