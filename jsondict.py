from pathlib import Path
import json
import os

class jsondict(dict):

    def __init__(self, *args, **kwargs):
        self.filename = Path.cwd() / "jsondict.json"

        if "filename" in kwargs:
            self.filename = Path(kwargs["filename"]).resolve()

        super().__init__(*args, **kwargs)

        self._loadfromjson()

    def _loadfromjson(self):
        if self.filename.exists():
            self.update(json.loads(open(str(self.filename)).read()))
        
    def save(self):
        with open(str(self.filename),"w") as f:
            f.write(json.dumps(self))
