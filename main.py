from collect_data import run
import os
import schedule
import time

if __name__ == '__main__':
    schedule.every(2).minutes.do(run)

    try:
        print("Press Ctrl+C to exit")
        while True:
            schedule.run_pending()
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        schedule.clear()