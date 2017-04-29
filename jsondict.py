from pathlib import Path
import json
import os

class jsondict(dict):
    def __init__(self, filename=None):
        super().__init__()

        self.filename = None

        # try to open the file before we try to resolve it's path and convert to Pathlib.Path type
        if filename != None:
            if not os.path.exists(filename):
                self.filename = Path.cwd() / filename
                self.save()         # if we didn't exist, this creates the proper file for later
            else:
                self.filename = Path(filename).resolve()


        self._loadfromjson()

    def _loadfromjson(self):
        if self.filename and self.filename.exists():
            self.update(json.loads(open(str(self.filename)).read()))
        
    def save(self):
        if self.filename:
            with open(str(self.filename),"w") as f:
                f.write(json.dumps(self))



# basic tests
if __name__=="__main__":
    f = "test.json"
    
    # put tests here
    d = jsondict()
    d['key'] = "value"
    d.save()

    del(d)
    
    if os.path.exists(f):
        os.remove(f)
    d = jsondict(f)
    d['key'] = "value"
    d['string'] = "String Value"
    d['int'] = 10
    d["float"] = 10.991
    d.save()
    del(d)
    d = jsondict(f)
    print (d)
    del(d)

