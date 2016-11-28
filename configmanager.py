from tinydb import TinyDB, Query
import pathlib  

class DBSettings(dict):
    
    def __init__(self, settingsdb, *args, **kwargs):
        self.db = settingsdb
        super().__init__(*args, **kwargs)

        self._LoadAllSettings()

    def __setitem__(self, key, value):
        q = Query()
        if self.db.get(q.key == key):
            self.db.update( {"key":key, "value": value}, q.key==key )
        else:
            self.db.insert( {"key":key, "value": value} )

        super().__setitem__(key,value)

    def _LoadAllSettings(self):
        q = Query()
        for i in self.db.search(q.key.exists()):
            dict.__setitem__(self, i["key"], i["value"])

class ConfigManager(object):

    _SAVEASATTRIBUTE = ["urlpath", "setup", ]

    DBNAME = "db.json"

    def __init__(self, LocationForDB=None):
        self.urlpath = None

        self.db = None                      # TinyDB DB
        self.setup = False                  # are we setup yet?

        if LocationForDB != None:
            self._open(LocationForDB)
        else:
            raise Exception("Need a DB path")

        self.settings = DBSettings(self.db) 
        self._LoadAttributes()

    def _open(self, LocationForDB):
        DBFilePath = pathlib.Path(LocationForDB).resolve()
        DBFileToOpen = DBFilePath / self.DBNAME

        try:
            self.db = TinyDB(str(DBFileToOpen))
            # self.setup = True
            self.dbpath = DBFilePath
        except:
            self.setup = False
            raise 

    def __setattr__(self, name, value):
        if hasattr(self, "db"):
            if name in self._SAVEASATTRIBUTE:
                self._SaveAttributeToDB(name, value)

        super().__setattr__(name, value)

    def _SaveAttributeToDB(self, name, value):
        if self.db != None:
            q = Query()
            if self.db.get(q.attribute == name):
                self.db.update( {"attribute":name, "value": value}, q.attribute==name )
            else:
                self.db.insert( {"attribute":name, "value": value} )

    def _LoadAttributes(self):
        q = Query()
        for a in self._SAVEASATTRIBUTE:
            E = self.db.get(q.attribute == a)
            if E == None:
                pass
            else:
                setattr(self, a, E["value"])

    def Load(self):
        self._LoadAttributes()

    # def _saveattributes(self):
    #     q = Query()
    #     for a in self.ATTRIBS:
    #         if self.db.get(q.attribute == a):
    #             self.db.update({"attribute":a, "value": getattr(self, a)}, q.attribute==a )
    #         else:
    #             self.db.insert({"attribute":a, "value": getattr(self, a)})
    # def initialize(self, LocationForDB):
    #     if not self.setup:
            # if pathlib.Path(LocationForDB).is_dir():
    #             self._CreateDB(LocationForDB)
    #             self._open(LocationForDB)
    #         else:
    #             raise Exception("Cannot initialize at %s" % LocationForDB)
    # def _CreateDB(self, LocationForDB):

    #     tempdb = None
    #     temppath = None

    #     try:
    #         temppath = pathlib.Path(LocationForDB).resolve()
    #         tempdbname = temppath / DBNAME
    
    #         if not tempdbname.exists(): 
    #             tempdb = TinyDB(str(tempdbname) )
    #             tempdb.purge_tables()
    #             tempdb.insert({"LocationForDB" : str(temppath)} )
    #         else:
    #             raise Exception("Unable to create DB")
    #     except:
    #         raise

    #     tempdb.close()

    # def _OpenDB(self, FileToOpen):
    #     self.db = TinyDB(str(FileToOpen))


# class CfgManager(object):
#     dbpath = None
#     urlpath = None 

#     _attribs = ["dbpath", "urlpath"]
#     settings = {}

#     def __init__(self):
#         self.db = None
#         self.db = TinyDB(DBNAME)

#     def ShowAttributes(self):
#         for a in self._attribs:
#             print (getattr(self, a))

#     def SaveAttributes(self):
#         q = Query()
#         for a in self._attribs:
#             if self.db.get(q.attribute == a):
#                 self.db.update({"attribute":a, "value": getattr(self, a)}, q.attribute==a )
#             else:
#                 self.db.insert({"attribute":a, "value": getattr(self, a)})
        
#     def LoadAttributes(self):
#         q = Query()
#         for a in self._attribs:
#             E = self.db.get(q.attribute == a)
#             if E == None:
#                 pass
#             else:
#                 setattr(self, a, E["value"])
