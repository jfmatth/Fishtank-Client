import time
import os
import logging

from conf import logconfig
from conf import constants

from dbdict import DBDict
from xdb.tables import dbInit

# list of all modules we'll call from scheduler.
from jobs import test1

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_SCHEDULER_SHUTDOWN

logger = logging.getLogger(__name__)
settings = DBDict(constants.SETTING_FILE)

def setup():
    # setup the environment, DB's, etc.
    dbInit(constants.SETTING_FILE)

def main():
    logger.info("loading scheduler")
    scheduler = BackgroundScheduler()
    
    # here is where all jobs / listeners are added.
    scheduler.add_job(test1.main, 'interval', seconds=3)
    scheduler.add_listener(test1.listener, EVENT_SCHEDULER_SHUTDOWN)

    logger.info('starting scheduler')
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
            logger.info("waiting...")
            
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    setup()
    main()