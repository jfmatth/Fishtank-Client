# find all the files that haven't been encrypted yet, and encrypt them.

import logging

from dbdict import DBDict
from conf import constants

logger = logging.getLogger(__name__)
settings = DBDict(constants.SETTING_FILE)

_shutdown = False

def shutdown(event):
    logger.info("shutdown signal received")
    _shutdown = True
    
def main():
    logger.info("main starting")
    pass
    
if __name__ == "__main__":
    shutdown = False
    main()
    
    