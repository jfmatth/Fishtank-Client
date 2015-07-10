from backup import Backup

class MyBackup(Backup):
    
    def _dirglob(self):
        return [] + [self._archivepath()] + ["C:/temp/dir3",]
    
    def _drives(self):
        return ["C:\\Users\\jmatthew\\Downloads", "c:/temp",]

    def _fileglob(self):
        return ["*.pyc", "*.dll", "*.csv", "*.iso"]
    
if __name__ == "__main__":
    
    b = MyBackup("C:/temp/archive")
    
    b.main()