

from tinydb import TinyDB, Query
import pathlib  

DBNAME = "db.json"

class MyDict(object):
    a = 1
    b = 2

    _attribs = ["a", "b"]
    settings = {}

    def __init__(self):
        self.db = TinyDB(DBNAME)

    def ShowAttributes(self):
        for a in self._attribs:
            print (getattr(self, a))

    def SaveAttributes(self):
        q = Query()
        for a in self._attribs:
            if self.db.get(q.attribute == a):
                self.db.update({"attribute":a, "value": getattr(self, a)}, q.attribute==a )
            else:
                self.db.insert({"attribute":a, "value": getattr(self, a)})
        
    def LoadAttributes(self):
        q = Query()
        for a in self._attribs:
            E = self.db.get(q.attribute == a)
            if E == None:
                pass
            else:
                setattr(self, a, E["value"])

class ConfigManager(object):
    dbpath = None
    urlpath = None

    def __init__(self, LocationForDB=None):
        self.db = None                      # TinyDB DB
        self.setup = False                  # are we setup yet?
        self.settings = []                  # a dict to hold client settings
        self.settingstable = None

        if LocationForDB != None:
            self._open(LocationForDB)

    def _open(self, LocationForDB):
        DBFilePath = pathlib.Path(LocationForDB).resolve()
        DBFileToOpen = DBFilePath / DBNAME
        try:
            if DBFileToOpen.exists():
                self._OpenDB(DBFileToOpen)
                self._loadsettings()

                self.setup = True
                self.dbpath = DBFilePath
            else:
                raise Exception("database does not exist, %s" % DBFileToOpen ) 
        except:
            self.setup = False
            raise 

    def _CreateDB(self, LocationForDB):

        tempdb = None
        temppath = None

        try:
            temppath = pathlib.Path(LocationForDB).resolve()
            tempdbname = temppath / DBNAME
    
            if not tempdbname.exists(): 
                tempdb = TinyDB(str(tempdbname) )
                tempdb.purge_tables()
                tempdb.insert({"LocationForDB" : str(temppath)} )
            else:
                raise Exception("Unable to create DB")
        except:
            raise

        tempdb.close()

    def _OpenDB(self, FileToOpen):
        self.db = TinyDB(str(FileToOpen) )
        self.settingstable = self.db.table("settings")

    def _loadsettings(self):
        pass

    def initialize(self, LocationForDB):
        if not self.setup:
            if pathlib.Path(LocationForDB).is_dir():
                self._CreateDB(LocationForDB)
                self._open(LocationForDB)