import json
import logging
from backup import BackupManager
import pathlib

logger = logging.getLogger(__name__)

def stopcallback(instance):
    print (instance.CurrentFile)
    return False

s = json.loads(open("settings.json").read() )

backup = BackupManager( s["archivepath"] )

backup.drives = s['drives']
backup.dirglob = s['dirglob']
backup.fileglob = s['fileglob']

backup._stop = stopcallback

print(backup)
