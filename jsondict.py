from pathlib import Path
import json
import os

JSONFILE = "jsondict.json"

class jsondict(dict):

    def __init__(self, filename=None):
        self.filename = None

        # try to open the file before we try to resolve it's path and convert to Pathlib.Path type
        if filename != None:
            if not os.path.exists(filename):
                self.filename = Path.cwd() / filename
            else:
                self.filename = Path(filename).resolve()

        super().__init__()

        self._loadfromjson()

    def _loadfromjson(self):
        if self.filename and self.filename.exists():
            self.update(json.loads(open(str(self.filename)).read()))
        
    def save(self):
        if self.filename:
            with open(str(self.filename),"w") as f:
                f.write(json.dumps(self))
