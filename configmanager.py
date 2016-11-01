from tinydb import TinyDB, Query
import pathlib  

class setting(object):

    def __init__(self, LocationForDB=None):
        self.dbfile = None
        self.db = None
        self.settingstable = None
        self.setup = False

        if LocationForDB != None:
            self._setup(LocationForDB)

    def _setup(self, LocationForDB):
        try:
            self.dbfile = pathlib.Path(LocationForDB).resolve() / "db.json"
            self.db = TinyDB(str(self.dbfile) )
            self.settingstable = self.db.table("settings")
            self.setup = True
        except:
            self.setup = False

    def __getitem__(self, key):
        if self.setup:
            q = Query()
            return self.settingstable.search(q.setting==key)
        else:
            return None

    def initialize(self, LocationForDB):
        if not self.setup:
            LocationForDB = pathlib.Path(LocationForDB).resolve()

            self._setup(LocationForDB)
            self.db.purge_tables()

            self.db.insert({"LocationForDB":str(LocationForDB)})
        else:
            raise Exception("Already Initialized")

