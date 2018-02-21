import pathlib
import os
import platform



class Config(object):
    # base meta class for all config types that return configuration info
    # this will derive all other classes based on Operating system

    def __init__(self):
        pass

    def ArchivePath(self):
        return pathlib.Path(os.path.abspath(__file__) ) + "archives"

    def Platform(self):
        return platform.system()

class WindowsConfig(Config):
    pass

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
    
    assert 0, "Cannot deterimine platform" + p

if __name__ == "__main__":
    # 
    x = ConfigManager()
    print(x.Platform())

