# find all files that are encrypted but not uploaded yet, and upload

import logging
import re
import os
import zipfile
import time
import pathlib

import dbdict
import constants
import archive

logger = logging.getLogger(__name__)
settings = dbdict.DBDict(constants.SETTING_FILE)


def listener(event):
    logger.debug("shutting down")

def main():
    logger.info(__name__)
    
    settings.refresh()
    print settings


class BackupNew():

    def __init__(self):
        logger.debug("Initializeing %s" % self.__class__)

        self.settings = None        # settings dict






    # _dirglob - returns the directories to exclude from backup.  Should be retrieved from settings.  We always exclude ourself 
    #    
    def _dirglob(self):
        return [] + [self._archivepath()]


    # _fileglob - returns the file GLOB pattern to exclude from backup.  This should be retreived from the settings DICT.
    #
    def _fileglob(self):
        return ["*.pyc", "*.dll", "*.csv"]


    # _drives - returns a list of drives to backup, this should come from win32 properties.
    #
    def _drives(self):
        # returns back a list of drives to backup.
        return ["C:\\temp",]



    # globexcluded - See if glob matches any of the glob(s)
    # 
    def globexcluded(self, glob, globitem):
        # check to see if this item matches the list of globs
        for x in glob:
            if globitem.match(x):
                return True
        else:
            return False


    # filebackuplist - Yield only files in this folder that are OK to backup to the archive.
    #
    def filebackuplist(self, path):
        # path is a pathlib path, so it's iterable for all files.

        for f in path.glob("*"):
            # don't backup directories, that's above us, we are only interested in files.
            if f.is_dir():
                continue
            
            # is the is in the exclusion list?
            if self.globexcluded(self._fileglob(), f):
                continue

            # is it already backed up?
            if self.archive.check(f):
                continue

            yield f.resolve()


    # addfoldertoarchive - Iterrate over all files in this folder and see if we should add them to the archive.
    #
    def addfoldertoarchive(self, folder):
        # make sure we have a Pathlib object that has the fullpath
        p = pathlib.Path(folder).resolve()
        
        if not self.globexcluded(self._dirglob(), p):
            
            for f in self.filebackuplist(p):
                self.addfiletoarchive(f)


    def run(self):
        logger.info("starting run()")

        for drive in self._drives():
            logger.info("drive %s" % drive)
            
            for root, dirs, files in os.walk(drive):
                
                # add the current directory too.
                self.addfoldertoarchive(root)

                logger.info("root = %s" % root)
                loprint "dirs = %s" % dirs
                
                for d in dirs:
                    self.addfoldertoarchive(os.path.join(root,d))

        print "closing archive"
        if self.archive:
            self.archive.close()


if __name__ == "__main__":
    main()