import json
import logging
# from jsondict import jsondict

from backupmanager import BackupManager
from config import ConfigManager

logger = logging.getLogger(__name__)

def stopcallback(instance):
    print (instance.CurrentFile)
    print (instance.archive.size)
    print (instance.zi)
    return False

# config = jsondict(filename="config.json")
# print (config)

config = ConfigManager()

# backup = BackupManager( s["archivepath"] )
backup = BackupManager( config )

# backup.drives = config['drives']
# backup.dirglob = config['dirglob']
# backup.fileglob = config['fileglob']

backup._stop = stopcallback

print(backup)

backup.run()
