### config.py 
Configuration manager class.

- Instantiate an instance of this to read in the config file and settings, used by all modules.
- platform specific, but you can call it with a specific platform 
    - Windows config file = defaultWindows.json
    - Linux config file = defaults.json (not implemented yet)
- This will read from the config file and allow users of the object to read config items

### archivemanager.py
Keeps track of archives (zip files) via a SQLITE DB.  Uses PEEWEE as ORM

Once instantiated, you just call obj.fileadd(file).  The DB is checked to see if the file is already there and if not, will add it accordingly.

### backupmanager.py
Main backup class.  

- The config object, tells the backup manager what folders to backup, what folders and files are excluded and what 'drives' to backup (drives = folders).

once instantiated, call obj.run() to execute.  

There is a stop callback mechanism that will be documented later.
