import json
import logging
from backup import BaseBackupManager
import pathlib

logger = logging.getLogger(__name__)


s = json.loads(open("settings.json").read() )

backup = BaseBackupManager( s["archivepath"] )



