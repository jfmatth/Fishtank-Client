# find all files that are encrypted but not uploaded yet, and upload

import logging
import os
import pathlib

from archivemanager import ArchiveManager
from config import cfg

logger = logging.getLogger(__name__)

class BackupManager(object):
    """
    This is the base abstract class to get the backups working.  You should inherit from this, overriding
    the various classes to make it work.  Without overriding things, nothing will get backed up.
    you should override the following:
        _stop - this is a callable to return true if backups should stop, i.e. service end or ctrl-c
    """

    def __init__(self):
        logger.debug("BackupManager: Initializing")

        self.archive = ArchiveManager()
        self.stopbackup = False

        self.drives =cfg.RootFolders()      # What drives / root folders should we be backing up
        self.dirglob = cfg.folders           # what folders are excluded
        self.fileglob = cfg.extensions       # what extensions to exclude

        self.CurrentFolder = None
        self.CurrentFile = None

        logger.debug("BackupManager: archivepath=%s" % self.archive.path)
        logger.debug("BackupManager._dirglob() = %s" % self.dirglob)
        logger.debug("BackupManager:_drives() = %s" % self.drives)

    def __str__(self):
        r = "drives = %s\n" % self.drives
        r+= "dirglob = %s\n" % self.dirglob
        r+= "fileglob = %s\n" % self.fileglob

        return r

    def __repr__(self):
        return self.__str__()

    def _stop(self, instance):
        """
        A stub callback for this class, most likely overridden.
        """
        # _stop - A simple callback to know if we should stop the whole process.
        return False

    def checkstop(self):
        """
        called when we are seeing if we should stop this whole process
        """
        if hasattr(self._stop, "__call__"):

            if self.stopbackup or self._stop(self):
                self.stopbackup = True
                return True
            else:
                return False

    def globexcluded(self, glob, globitem):
        """ check to see if this item matches the list of globs """
        for x in glob:
            if globitem.match(str(x)):
                logger.debug("BackupManager: Skipping excluded %s" % globitem)
                return True
        else:
            return False

    def filebackuplist(self, path):
        """
        Yield only files in this folder that are OK to backup to the archive
        """
        assert isinstance(path, pathlib.Path)

        for f in path.glob("*"):
            # don't backup directories, that's above us, we are only interested in files in this folder.
            if f.is_dir():
                continue

            # is the is in the exclusion list?
            if self.globexcluded(self.fileglob, f):
                continue

            self.checkstop()

            yield f

    def addfoldertoarchive(self, folder):
        """
        Iterrate over all files in this folder and see if we should add them to the archive.
        """

        p = pathlib.Path(folder).resolve()

        logger.debug("BackupManager: addfoldertoarchive.p = %s" % p)

        if not self.globexcluded(self.dirglob, p):
            self.CurrentFolder = folder

            for f in self.filebackuplist(p):
                self.CurrentFile = f

                if self.stopbackup: break

                self.archive.fileadd(f)

    def run(self):
        """
        Called to start the backups and run until everything is backed up, or _stop() returns true
        (via stopbackup)
        """
        self.dirglob = [self.archive.path] + self.dirglob  # don't backup the archives to the archives :)

        logger.debug("BackupManager: run()")
        for drive in self.drives:
            logger.debug("BackupManager: drive = %s" % drive)

            if self.stopbackup: break

            for root, dirs, files in os.walk(drive):

                if self.stopbackup: break

                # add the current directory too.
                self.addfoldertoarchive(root)

                for d in dirs:
                    self.addfoldertoarchive( os.path.join(root,d) )
                    if self.stopbackup:
                        break

        if self.archive:
            self.archive.close()