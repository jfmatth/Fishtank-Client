import logging

from settingmgr.dict import DBDict
from conf import constants

logger = logging.getLogger(__name__)
settings = DBDict(constants.SETTING_FILE)

def listener(event):
    logger.info("test1.py - shutting down")

def main():
    logger.info("test1")
    settings.refresh()
    print settings
    
if __name__ == "__main__":
    main()
    
    