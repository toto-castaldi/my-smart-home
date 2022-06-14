import time
import schedule
import utils
import tasmota
import lifx

logger = utils.init_log()

def tick_job():
    logger.info("tick...")

if __name__ == '__main__':        
    schedule.every(1).minutes.do(tick_job)

    while True:
        schedule.run_pending()
        time.sleep(1)