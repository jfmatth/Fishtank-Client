import json
import logging
# from jsondict import jsondict

from backupmanager import BackupManager
from config import cfg

logger = logging.getLogger(__name__)

def stopcallback(instance):
    print (instance.CurrentFile)
    print (instance.archive.size)
    return False

# config = jsondict(filename="config.json")
# print (config)

# backup = BackupManager( s["archivepath"] )
backup = BackupManager()

# backup.drives = config['drives']
# backup.dirglob = config['dirglob']
# backup.fileglob = config['fileglob']

backup._stop = stopcallback

print(backup)

backup.run()
