

from tinydb import TinyDB, Query
import pathlib  


class ConfigManager(object):
    dbpath = None
    urlpath = None

    def __init__(self, LocationForDB=None):
        self.db = None                      # TinyDB DB
        self.setup = False                  # are we setup yet?
        self.settings = []                  # a dict to hold client settings

        if LocationForDB != None:
            self._open(LocationForDB)

    def _open(self, LocationForDB):
        self.dbfile = pathlib.Path(LocationForDB).resolve() / "db.json"
        try:
            if self.dbfile.exists():
                self._OpenDB()
                self._loadsettings()
                self.setup = True
            else:
                raise Exception("Issue opening DB") 
        except:
            self.setup = False
            raise 

    def _CreateDB(self):
        if self.dbfile != None amd self.dbfile.exists():
            self.db = TinyDB(str(self.dbfile) )
            self.db.purge_tables()
            self.db.insert({"LocationForDB" : str(LocationForDB)} )
            self.settingstable = self.db.table("settings")
        else:
            raise Exception("Cannont have blank dbfile path")

    def _OpenDB(self):
        if self.dbfile != None:
            self.db = TinyDB(str(self.dbfile) )
            self.settingstable = self.db.table("settings")
        else:
            raise Exception("Blank files not allowed")

    def _loadsettings(self):
        print("load settings")
        pass

    def initialize(self, LocationForDB):
        validlocation = pathlib.Path(LocationForDB).resolve()
        if not self.setup:
            self.dbfile = pathlib.Path(LocationForDB).resolve()

            self._CreateDB()
        else:
            raise Exception("Already Initialized")



