import pathlib
import os
import platform
import json

basepath = pathlib.Path(os.path.abspath(os.path.dirname(__file__) ) )

class Config(object):
    # base meta class for all config types that return configuration info
    # this will derive all other classes based on Operating system

    def __init__(self):
        # common init routine, should pull down any setup necessary from server
        self.settings = {}
        self.defaultsfile = "defaults.json"

        self._Setup()
        self._LoadDefaults()

    def __getattr__(self, name):
        # fallback if we are looking from something from settings
        return self.settings.get(name, None)

    def _Setup(self):
        # we set any local stuff here so as not to have to override __init__
        pass

    def _LoadDefaults(self):
        # load a default file with settings?
        print("Loading defaults from %s" % self.defaultsfile)

        if self.defaultsfile and pathlib.Path(self.defaultsfile).exists():
            self.settings = json.loads(open(str(self.defaultsfile)).read() )
        else:
            print("no settings file %s exists" % self.defaultsfile)

    def ArchivePath(self):
        return basepath / "archives"

    def Platform(self):
        return platform.system()

    def RootFolders(self):
        # return a list of root folders to backup, these might be:
        # C:/users/, /home, etc, depending on the platform
        return self.settings.get("RootFolders", None)


class WindowsConfig(Config):

    def _Setup(self):
        self.defaultsfile = "defaultWindows.json"

class OSXConfig(Config):
    pass

class LinuxConfig(Config):
    pass


# The ConfigManager returns a config object based on the running OS.  Most properties / methods
# should be defined in the meta class and inherited down to the individual OS specific class, but
# can be overriden if necessary
def ConfigManager():

    p = platform.system()

    if  p == "Windows":
        return WindowsConfig()

    if p == "Linux":
        return LinuxConfig()
    
    assert 0, "Platform %s not supported" % p



if __name__ == "__main__":
    # 
    x = ConfigManager()
    print("Platform: %s" % x.Platform())
    print("ArchivePath: %s" % x.ArchivePath())

