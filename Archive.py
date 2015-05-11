import zipfile
import uuid
import pathlib
import zlib
import logging
import os
import db

logger = logging.getLogger(__name__)

# pointers to DB stuff
Backup = db.Backup
File = db.File

class ArchiveManager():
    # manage an archive of files and the DB behind them 
    def __init__(self, archivepath, name="archive.db"):

        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of arhive
        self.limit = 100000             # limit of Archive size
        self.backup_record = None       # FK pointer

        self.path = pathlib.Path(archivepath).resolve()
        logger.debug("path = %s" % self.path)

        # Initialize the DB (peewee).
        logger.debug("calling dbInit()")
        db.dbInit( str(self.path / name) )     #  DUDE, I love pathlib.


    def close(self):
        self._closearchive()
        
        return True
        
    
    def _crc(self, f):
        prev = 0
        for line in open(f,"rb"):
            prev = zlib.crc32(line, prev)

        return "%X"%(prev & 0xFFFFFFFF)

    def _closearchive(self):
        logger.debug("closing archive")
        if self.archive:
            self.archive.close()
        
        self.size = 0                   # current size of archive
        self.archive = None             # current archive (zip) file being used.
        self.name = None                # current name of arhive
        self.backup_record = None       # FK pointer


    # _newarchive - setup a new archive, close the old one if necessary.
    #
    def _newarchive(self):
        self._closearchive()
            
        self.name = (self.path / ( str( uuid.uuid4()) + ".zip") ).as_posix()
        self.archive = zipfile.ZipFile(str(self.name), "w", compression=zipfile.ZIP_DEFLATED)

        # create a new Backup entry in the DB.    
        self.backup_record = Backup.create(fullpath = self.name,
                                           encrypted = False, 
                                           uploaded = False)

        logger.info("Created new backup backup record %s" % self.backup_record)        
        return 


    # checkarchive - Make sure this archive is good to go.
    #
    def checkarchive(self):
        if self.archive == None or self.size > self.limit:
            self._newarchive()
            

    # addfile - Add to the DB and ZIP file.
    #
    def addfile(self, f1):
        #
        # f - (pathlib.Path) File to add to the archive, only one file at a time :)
        #

        self.checkarchive()

        try:
            with db.database.atomic():
                f = f1.resolve()
                
                logger.info("adding %s to DB/Archive" % str(f))
    
                self.archive.write( str(f) )
                self.size += f.stat().st_size
    
                # keep the times as integers for simplicity sake.
                File.create(
                            backup   = self.backup_record, 
                            
                            fullpath = f.as_posix(),
                            filename = f.name, 
                            size = f.stat().st_size,
                            modified = f.stat().st_mtime, 
                            accessed = f.stat().st_atime, 
                            created  = f.stat().st_ctime,
                            crc      = self._crc(f.as_posix() ) 
                           )
                
                # everything worked, let em know.
                return True
                
        except Exception, e:
            raise


    # findfind -See if this file (f) already is in the DB
    # 
    def findfile(self, f):

        filename = f.resolve().as_posix()

        try:
            # search DB by name
            try:
                logger.debug("checking name")
                File.get(File.fullpath == filename)

                logger.debug("checking mtime")
                File.get(File.fullpath == filename,
                         File.modified == f.stat().st_mtime
                         )

                logger.debug("Searching by CRC")
                File.get(File.fullpath == filename,
                         File.crc == self._crc(filename)
                        )
            
            except:
                logger.debug("%s Not Found in DB" % filename)
                return False

            else:
                # if we get here, then it's the same file, so return True as an exclusion.
                logger.debug("%s Found in DB" % filename)
                return True
        
        except:
            logger.error("Error in dbexcluded")



    def delete_archive(self, name):

        self._closearchive()

        if os.path.exists(name):
       
            # remove archive from DB and file system.
            try:
                os.remove(name)
                Backup.select().where(Backup.fullpath == name).get().delete_instance(recursive=True)
    
                return True
            except:
                
                raise
        else:
            return False
    
    def delete_file(self, f):
        try:
            logger.debug("trying to delete File record %s" % f)
            File.get(File.fullpath == f).delete_instance()
        except Exception, e:
            logger.error(e)

    
    # Generators to return backup records of certain types.
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

            