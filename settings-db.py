from tinydb import TinyDB, Query

import pathlib  # we like pathlib.

class setting(object):

    def __init__(self, LocationForDB=None):
        self.dbfile = None
        self.db = None
        self.settingstable = None

        if LocationForDB != None:
            self._setup(LocationForDB)

    def _setup(self, LocationForDB):
        self.dbfile = pathlib.Path(LocationForDB).resolve() / "db.json"
        self.db = TinyDB(str(self.dbfile) )
        self.settingstable = self.db.table("settings")

    def initialize(self, LocationForDB):
        LocationForDB = pathlib.Path(LocationForDB).resolve()

        self._setup(LocationForDB)
        self.db.purge_tables()

        self.db.insert({"LocationForDB":str(LocationForDB)})

    def __setitem__(self, key, value):
        self.settingstable.insert( {"setting": key, "value":value} )

    def __getitem__(self, key):
        q = Query()
        return self.settingstable.search(q.setting==key)
