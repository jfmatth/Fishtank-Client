import zipfile
import pathlib
import logging
import os
import uuid

from db import database, Backup, File
from config import cfg

logger = logging.getLogger(__name__)

class ArchiveManager():
    """
    Manager of Archives via DB layout above
    """

    def __init__(self):

        logger.debug("ArchiveManager: __init__")

        self.maxsize = cfg.maxfilesizekb

        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of archive
        self.backuprecord = None        # FK pointer

        try:
            ap = cfg.ArchivePath()
            pathlib.Path(ap).mkdir(parents=True, exist_ok=True)
            self.path = pathlib.Path(ap).resolve()
        except:
            raise

        logger.debug("ArchiveManager .path = %s" % self.path)

        # initialize our environemnt if we need to, but connect if its there
        database.init(str(self.path / "archive.db") )
        database.connect()
        database.create_tables([Backup], safe=True)
        database.create_tables([File], safe=True)

        self._validate()

    def _validate(self):
        """
        validate when all the archives you think you have, remove the ones you don't
        """
        logger.debug("ArchiveManager: validating all archives.")

        self.close()

        for a in self.all_archives():

            # if the archive doesn't exist, remove it from the DB and all its referenced files
            if not os.path.exists(a.fullpath):
                logger.warning("ArchiveManager: removing reference to non-existent archive %s" % a.fullpath)
                a.delete_instance(recursive=True)

    def close(self):
        """
        Close the current archive we have open
        """
        logger.debug("ArchiveManager: close()")
        self._closearchive()

        return True

    def _crc(self, f):
        """
        return the CRC of a file

        NOT CURRENTLY RUNNING CRC for now due to alpha code
        """
#
#
#         prev = 0
#         for line in open(f,"rb"):
#             prev = zlib.crc32(line, prev)
#
#         return "%X"%(prev & 0xFFFFFFFF)

        return 0

    def _closearchive(self):
        """
        Closes the actual archive if we have one open, and reset's the various internal counters, etc.
        """
        if self.archive:
            logger.debug("ArchiveManager: Saving DB archive record")
            self.backuprecord.ready = True
            self.backuprecord.save()

            logger.debug("ArchiveManager: closing archive file")
            self.archive.close()

        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of arhive
        self.backuprecord = None       # FK pointer

    def _newarchive(self):
        """
        Setup a new archive, close the old one if necessary

        NOTE:   might improve the resilency of this code to use an atomic transaction around the 
                zip file creation.
        """
        self._closearchive()

        self.name = (self.path / ( str( uuid.uuid4()) + ".zip") ).as_posix()
        self.archive = zipfile.ZipFile(str(self.name), "w", compression=zipfile.ZIP_DEFLATED)
        logger.debug("ArchiveManager: create new archive file %s" % self.name)

        # create a new Backup entry in the DB.
        self.backuprecord = Backup.create(fullpath = self.name,
                                          ready = False,
                                          encrypted = False,
                                          uploaded = False)

        logger.info("ArchiveManager: Created new backup backup record %s" % self.backuprecord)


    def checkarchive(self):
        """
        Make sure this archive meets our criteria and we don't need a new one
        """
        if self.archive == None or self.size > self.maxsize:
            self._newarchive()

    def fileadd(self, filetoadd):
        """
         Add to the DB and ZIP file.
        """
        self.checkarchive()

        # handle any kind of file coming in, pathlib or str :)
        f = pathlib.Path(filetoadd).resolve()

        try:

            if not self.filefind(f):

                with database.atomic():
                    logger.debug("ArchiveManager: adding %s to DB/Archive" % f)

                    self.archive.write( str(f) )
                    self.size += f.stat().st_size

                    # keep the times as integers for simplicity sake.
                    File.create(
                                backup   = self.backuprecord,

                                fullpath = f.as_posix(),
                                filename = f.name,
                                size     = f.stat().st_size,
                                modified = f.stat().st_mtime,
                                accessed = f.stat().st_atime,
                                created  = f.stat().st_ctime,
                                crc      = self._crc(f.as_posix() )
                               )

                    # everything worked, let em know.
                    return True
            else:
                # we found a matching file, so return True anyway
                logger.debug("ArchiveManager: Skipping found file %s" % f)
                return True

        except Exception :
            raise


    def filefind(self, filetofind):
        """
        :param filetofind: file to find in the DB
        :return: True - found, False - not there
        """
        f = pathlib.Path(filetofind).resolve()

        try:
            File.get(File.fullpath == f.as_posix(),
                     File.modified == f.stat().st_mtime,
                     File.crc == self._crc(f)
                     )
        except:
            logger.debug("ArchiveManager: %s Not Found in DB" % f)
            return False

        else:
            # if we get here, then it's the same file, so return True as an exclusion.
            logger.debug("ArchiveManager: %s Found in DB" % f)
            return True


    def archivedelete(self, nametodelete):
        """
        Delete an archive (zip) record and file.
        """
        logger.debug("ArchiveManager: archivedelete()")
        self._closearchive()

        if os.path.exists(nametodelete):

            # remove archive from DB and file system.
            try:
                logger.debug("ArchiveManager:Deleting file and record for %s" % nametodelete)
                os.remove(nametodelete)

                # YUCK - This could be better?
                Backup.select().where(Backup.fullpath == nametodelete).get().delete_instance(recursive=True)

                return True
            except:
                logger.debug("ArchiveManager:Exception during os.remove() or delete_instance for %s" % nametodelete)
                raise
        else:
            logger.debug("ArchiveManager: %s does not exist" % nametodelete)
            return False

    def filedelete(self, filetodelete):
        """
        Delete a single file from the DB
        """
        logger.debug("AM: filedelete() - filetodelete = %s" % filetodelete)

        f = pathlib.Path(filetodelete).resolve()

        try:
            logger.debug("ArchiveManager: trying to delete File record %s" % f)
            File.get(File.fullpath == f.as_posix()).delete_instance()
            return True

        except Exception:
            logger.debug("ArchiveManager: Exception during delete_instance for %s" % filetodelete)
            return False

    def all_files(self):
        """
        Return a list of all file records in this DB
        """
        return File.select()

    def all_archives(self):
        """
        Return a list of all backup records (zip entries)
        """
        return Backup.select()

    def unencrypted_archives(self):
        """
        Returns all Backup records that aren't encrypted yet
        """
        return Backup.select().where(Backup.encrypted == False)

    def uploadable_archives(self):
        # generator to give back all Backup records that uploaded = False
        return Backup.select().where(Backup.uploaded == False)
