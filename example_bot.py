from ci_stat.ci_stat import get_result
from ci_stat.feishu_bot import res_to_card, bot_post
from datetime import datetime, timedelta
import schedule
import time

def hourly_report():
    res = get_result(datetime.now, datetime.now - timedelta(hours=1), [])
    bot_post(res_to_card(res))

schedule.every().hour.do(hourly_report)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    pass