# config.py - configuration manager for Fishtank
# 
# A factory via the ConfigManager() to return a os-platform specific instance of a Config()
# object.  Most methods in the Config() parent do all the work, and a few of the sub-classes
# change simple behavior

import pathlib
import os
import platform
import json

import logging
logger = logging.getLogger(__name__)

basepath = pathlib.Path(os.path.abspath(os.getcwd() ) )

class _Config(object):
    """
    base class for all config types that return configuration info
    this will derive all other classes based on Operating system
    """
    def __init__(self):
        self.settings = {}
        self.defaultsfile = "defaults.json"

        self._Setup()
        self._LoadDefaults()

    def _Setup(self):
        """
        we set any local stuff here so as not to have to override __init__
        """
        pass

    def _LoadDefaults(self):
        """
        load a default file with settings?
        """
        logger.info("Loading defaults from %s" % self.defaultsfile) 

        try:
            if self.defaultsfile and pathlib.Path(self.defaultsfile).exists():
                with open(str(self.defaultsfile)) as f:
                    self.settings = json.loads(f.read() )
            else:
                logger.exception("no settings file %s exists" % self.defaultsfile)
        except:
            raise

    def __getattr__(self, name):
        """
        allow generic settings, but raise an exception if it's missing, instead of None
        """
        if not self.settings.get(name, None):
            raise Exception("config setting %s not found" % name)

        return self.settings[name]

    def ArchivePath(self):
        return basepath / "archives"

    def Platform(self):
        return platform.system()

    def RootFolders(self):
        """
        return a list of root folders to backup, these might be:
        C:/users/, /home, etc, depending on the platform
        """
        return self.settings.get("rootfolders", None)


class _WindowsConfig(_Config):

    def _Setup(self):
        self.defaultsfile = "defaultwindows.json"

# class _OSXConfig(_Config):
#     pass

class _LinuxConfig(_Config):
    pass


def ConfigManager(plat=None):
    """
    The ConfigManager returns a config object based on the running OS.  Most properties / methods
    should be defined in the meta class and inherited down to the individual OS specific class, but
    can be overriden if necessary

    plat - allows someone to override the platform for testing or other reasons
    """
    p = plat or platform.system()

    if  p == "Windows":
        return _WindowsConfig()

    if p == "Linux":
        return _LinuxConfig()
    
    raise Exception("Platform %s not supported" % p)

if __name__ == "__main__":
    x = ConfigManager()
    print("Platform: %s" % x.Platform())
    print("ArchivePath: %s" % x.ArchivePath())

