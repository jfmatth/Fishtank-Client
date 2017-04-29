import zipfile
import pathlib
import logging
import os
import uuid

import peewee

logger = logging.getLogger(__name__)

# Define the DB's we'll use in this module.
database = peewee.SqliteDatabase(None)
class basetable(peewee.Model):
    class Meta:
       database = database

# Backup - represents a ZIP file backup
class Backup(basetable):
    fullpath = peewee.CharField(unique=True, index=True)
    ready = peewee.BooleanField(index=True)
    encrypted = peewee.BooleanField(index=True)
    uploaded = peewee.BooleanField(index=True)

# File - each file in the ZIP, related to that parent record.
class File(basetable):
    backup = peewee.ForeignKeyField(Backup)

    fullpath = peewee.CharField(index=True)
    crc = peewee.CharField(index=True)
    filename = peewee.CharField()
    size = peewee.IntegerField()
    modified = peewee.DateField()
    accessed = peewee.DateField()
    created = peewee.DateField()

    class Meta:
        primary_key = peewee.CompositeKey("fullpath", "crc")



class ArchiveManager():
    # manage an archive of files and the DB behind them

    # def __init__(self, archivepath=os.curdir):
    def __init__(self, cfg):
        #:
        #: cfg - Dictionary of expected configuration parameters
        #   "archivepath"   - Full path to where to hold all archive files, default current directory os.curdir
        #   "maxsizeKB"     - Maximum size of archives before compression (.zip)

        # changed to use config variable (cfg) instead of one parameter.  Config is a dictionary

        logger.debug("AM: __init__")

        self.maxsize = cfg.get("maxsizeKB",10000 * 102400) # default of 100mb

        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of archive
        self.backuprecord = None        # FK pointer

        try:
            ap = cfg.get("archivepath", os.curdir)
            pathlib.Path(ap).mkdir(parents=True, exist_ok=True)
            self.path = pathlib.Path(ap).resolve()
        except:
            # make sure it exists
            raise

        logger.debug("AM .path = %s" % self.path)

        database.init(str(self.path / "archive.db") )
        database.connect()
        database.create_tables([Backup], safe=True)
        database.create_tables([File], safe=True)

        self._validate()

    def _validate(self):
        # validate when all the archives you think you have, remove the ones you don't
        logger.debug("AM: validating all archives.")

        self.close()

        for a in self.all_archives():

            # if the archive doesn't exist, remove it from the DB and all its referenced files
            if not os.path.exists(a.fullpath):
                logger.warning("AM: removing reference to non-existent archive %s" % a.fullpath)
                a.delete_instance(recursive=True)

    def close(self):
        logger.debug("AM: close()")
        self._closearchive()

        return True

    # not checking based on CRC right now.
    def _crc(self, f):
        return 0
#
#
#         prev = 0
#         for line in open(f,"rb"):
#             prev = zlib.crc32(line, prev)
#
#         return "%X"%(prev & 0xFFFFFFFF)

    def _closearchive(self):
        if self.archive:
            logger.debug("AM: Saving DB archive record")
            self.backuprecord.ready = True
            self.backuprecord.save()

            logger.debug("AM: closing archive file")
            self.archive.close()

        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of arhive
        self.backuprecord = None       # FK pointer


    # _newarchive - setup a new archive, close the old one if necessary.
    #
    def _newarchive(self):
        self._closearchive()

        self.name = (self.path / ( str( uuid.uuid4()) + ".zip") ).as_posix()
        self.archive = zipfile.ZipFile(str(self.name), "w", compression=zipfile.ZIP_DEFLATED)
        logger.debug("AM: create new archive file %s" % self.name)

        # create a new Backup entry in the DB.
        self.backuprecord = Backup.create(fullpath = self.name,
                                          ready = False,
                                          encrypted = False,
                                          uploaded = False)

        logger.info("AM: Created new backup backup record %s" % self.backuprecord)


    # checkarchive - Make sure this archive is good to go.
    #
    def checkarchive(self):
        # check to see if we have an existing archive (.zip) open or we are over our limit in filesize.
        if self.archive == None or self.size > self.maxsize:
            self._newarchive()

    # addfile - Add to the DB and ZIP file.
    #
    def fileadd(self, filetoadd):

        self.checkarchive()

        # handle any kind of file coming in, pathlib or str :)
        f = pathlib.Path(filetoadd).resolve()

        try:

            if not self.filefind(f):

                with database.atomic():
                    logger.debug("AM: adding %s to DB/Archive" % f)

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
                logger.debug("AM: Skipping found file %s" % f)
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
            logger.debug("AM: %s Not Found in DB" % f)
            return False

        else:
            # if we get here, then it's the same file, so return True as an exclusion.
            logger.debug("AM: %s Found in DB" % f)
            return True


    def archivedelete(self, nametodelete):
        logger.debug("AM: archivedelete()")
        self._closearchive()

        if os.path.exists(nametodelete):

            # remove archive from DB and file system.
            try:
                logger.debug("AM:Deleting file and record for %s" % nametodelete)
                os.remove(nametodelete)
                Backup.select().where(Backup.fullpath == nametodelete).get().delete_instance(recursive=True)

                return True
            except:
                logger.debug("AM:Exception during os.remove() or delete_instance for %s" % nametodelete)
                raise
        else:
            logger.debug("AM: %s does not exist" % nametodelete)
            return False


    def filedelete(self, filetodelete):

        logger.debug("AM: filedelete() - filetodelete = %s" % filetodelete)

        f = pathlib.Path(filetodelete).resolve()

        try:
            logger.debug("AM: trying to delete File record %s" % f)
            File.get(File.fullpath == f.as_posix()).delete_instance()
            return True

        except Exception:
            logger.debug("AM: Exception during delete_instance for %s" % filetodelete)
            return False


    def all_files(self):
        return File.select()

    def all_archives(self):
        return Backup.select()

    def unencrypted_archives(self):
        # a generator that returns all Backup records that aren't encrypted yet
        return Backup.select().where(Backup.encrypted == False)

    def uploadable_archives(self):
        # generator to give back all Backup records that uploaded = False
        return Backup.select().where(Backup.uploaded == False)
