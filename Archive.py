import zipfile
import uuid
import pathlib
import zlib

import peewee
from peewee import CompositeKey

db = peewee.SqliteDatabase(None)

class basetable(peewee.Model):
    class Meta:
        database = db


# Backup - represents a ZIP file backup
class Backup(basetable):
    fullpath = peewee.CharField(unique=True, index=True)
    encrypted = peewee.BooleanField(index=True)             # encrypted zips are called?
    uploaded = peewee.BooleanField(index=True)

    def All(self):
        return self.select()


# File - each file in the ZIP, related to that parent record.
class File(basetable):
    backup   =  peewee.ForeignKeyField(Backup)
    
    fullpath = peewee.CharField(index=True)
    crc      = peewee.CharField(index=True)
    filename = peewee.CharField()
    size     = peewee.IntegerField()
    modified = peewee.DateField()
    accessed = peewee.DateField()
    created  = peewee.DateField()
    
    class Meta:
        primary_key = CompositeKey("fullpath", "crc")


# Initialize all the tables
def dbInit(name="database.db"):
    db.init(name)
    db.connect()
    db.create_tables([Backup], safe=True)
    db.create_tables([File], safe=True)


class Manager():
    # manage an archive of files and the DB behind them 
    def __init__(self, archivepath, name="archive.db"):

        self.size = 0                   # current size of archive
        self.archive = None                 # current archive (zip) file being used.
        self.name = None                # current name of arhive
        self.limit = 100000             # limit of Archive size

        self.path = pathlib.Path(archivepath)

        # Initialize the DB (peewee).
        dbInit( str(self.path / name) )     #  DUDE, I love pathlib.

        self.backup_record = None       # FK pointer


    def _crc(self, f):
        prev = 0
        for line in open(f,"rb"):
            prev = zlib.crc32(line, prev)

        return "%X"%(prev & 0xFFFFFFFF)

    # _archivename - setup a new archive, close the old one if necessary.
    #
    def _newarchive(self):
        if self.archive:
            self.archive.close()
        
        self.size = 0
        self.name = self.path / ( str( uuid.uuid4()) + ".zip")
        self.archive = zipfile.ZipFile(self.archive_name, "w", compression=zipfile.ZIP_DEFLATED)

        # create a new Backup entry in the DB.    
        self.backup_record = Backup.create(Backup.fullpath == self.name)
        
        return 


    # checkarchive - Make sure this archive is good to go.
    #
    def checkarchive(self):
        if self.archive == None or self.size > self.limit:
            self._newarchive()
            

    # addfile - Add to the DB and ZIP file.
    #
    def addfile(self, f):
        #
        # f - (pathlib.Path) File to add to the archive, only one file at a time :)
        #

        self.checkarchive()

        with db.atomic():
            print "adding %s to DB/Archive" % f
            
            self.archive.write( str(f.as_posix() ) )
            self.archive_size += f.stat().st_size

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


    # findfind -See if this file (f) already is in the DB
    # 
    def findfile(self, f):

        filename = f.as_posix()

        try:
            # search DB by name
            try:
                print "checking name"
                File.get(File.fullpath == filename )

                print "checking mtime"
                File.get(File.fullpath == filename,
                         File.modified == f.stat().st_mtime)

                print "Searching by CRC"
                Files.get(File.fullpath == filename,
                          File.crc == self._crc(filename)
                          )
            
            except:
                print "%s Not Found in DB" % filename
                return False

            else:
                # if we get here, then it's the same file, so return True as an exclusion.
                print "%s Found in DB" % filename
                return True
        
        except:
            print "Error in dbexcluded"


