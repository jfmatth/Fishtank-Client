# find all files that are encrypted but not uploaded yet, and upload

import logging
import os
import pathlib

from archive import ArchiveManager

logger = logging.getLogger(__name__)

# BackupManager - This is the base abstract class to get the backups working.  You should inherit from this, overriding
# the various classes to make it work.  Without overriding things, nothing will get backed up.
class BackupManager(object):

    # def __init__(self, mypath = None):
    def __init__(self, cfg={}):
        #:
        #: cfg - Config dictionary of settings
        #:      "path" - path to where to store archives, default to os.curdir

        logger.debug("BM: Initializing")

        # self.archivepath = mypath or pathlib.Path(os.getcwd() )
        self.AMcfg = {
            "archivepath" : cfg.get("path", pathlib.Path(os.getcwd())),
        }

        self.archive = ArchiveManager(self.AMcfg)

        self.stopbackup = False
        self.dirglob = [self.archive.path]
        self.fileglob = []
        self.drives = []

        self.CurrentFolder = None
        self.CurrentFile = None

        logger.debug("BM: archivepath=%s" % self.archive.path)
        logger.debug("BM._dirglob() = %s" % self.dirglob)
        logger.debug("BM:_drives() = %s" % self.drives)

    def __str__(self):
        r = "drives = %s\n" % self.drives
        r+= "dirglob = %s\n" % self.dirglob
        r+= "fileglob = %s\n" % self.fileglob

        return r

    def __repr__(self):
        return self.__str__()


    # def _archivepath(self):
    #     # this will probably return a settings property at some point
    #     return self.archivepath
    #
    # # _dirglob - returns the directories to exclude from backup.  Should be retrieved from settings.  We always exclude ourself
    # #
    # def _dirglob(self):
    #     """
    #     Defines the list of folders to exclude from backup, including our own.
    #     :return:
    #     """
    #     return [] + [self._archivepath()]
    #
    # # _fileglob - returns the file GLOB pattern to exclude from backup.
    # #
    # def _fileglob(self):
    #     return []
    #
    # # _drives - returns a list of drives to backup
    # def _drives(self):
    #     # returns back a list of drives to backup.
    #     return []

    # _stop - A simple callback to know if we should stop the whole process.
    def _stop(self, instance):
        return False

    def checkstop(self):
        if hasattr(self._stop, "__call__"):

            if self.stopbackup or self._stop(self):
                self.stopbackup = True
                return True
            else:
                return False

    # globexcluded - See if glob matches any of the glob(s)
    #
    def globexcluded(self, glob, globitem):
        # check to see if this item matches the list of globs
        for x in glob:
            if globitem.match(str(x)):
                logger.debug("BM: Skipping excluded %s" % globitem)
                return True
        else:
            return False

    # filebackuplist - Yield only files in this folder that are OK to backup to the archive.
    #
    def filebackuplist(self, path):
        # path is a pathlib path, so it's iterable for all files.

        for f in path.glob("*"):
            # don't backup directories, that's above us, we are only interested in files in this folder.
            if f.is_dir():
                continue

            # is the is in the exclusion list?
            if self.globexcluded(self.fileglob, f):
                continue

            self.checkstop()

            yield f


    # addfoldertoarchive - Iterrate over all files in this folder and see if we should add them to the archive.
    #
    def addfoldertoarchive(self, folder):
        # make sure we have a Pathlib object that has the fullpath

        p = pathlib.Path(folder).resolve()

        logger.info("BM: addfoldertoarchive.p = %s" % p)

        if not self.globexcluded(self.dirglob, p):
            self.CurrentFolder = folder

            for f in self.filebackuplist(p):
                self.CurrentFile = f

                if self.stopbackup: break

                self.archive.fileadd(f)


    def run(self):

        logger.debug("BM: run()")
        for drive in self.drives:
            logger.debug("BM: drive = %s" % drive)

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