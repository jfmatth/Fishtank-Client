import unittest
import os
import sys
import pathlib

from archivemanager import ArchiveManager
from backupmanager import BackupManager
from config import ConfigManager

# aPATH = pathlib.Path("archives/").resolve()

filetotest = pathlib.Path(sys.executable)

class TestArchiveManager(unittest.TestCase):

    def setUp(self):
        self.config = ConfigManager()
        self.AM = ArchiveManager(self.config)

    def test_20_fileadd(self):
        
        self.assertTrue(self.AM.fileadd(filetotest))

        # adding the same file should also return true, even though it's not added.
        self.assertTrue(self.AM.fileadd(filetotest))

    def test_30_filefind(self):
        self.assertTrue(self.AM.filefind(filetotest) )

    def test_40_check_allarchives(self):

        for f in self.AM.all_archives():
            self.assertTrue( str(os.path.exists(f.fullpath)) )

    def test_60_addallpython(self):

        p = pathlib.Path(sys.executable).parent

        # add all files in the python directory
        for x in p.glob("*"):
            if not x.is_dir():
                self.assertTrue(self.AM.fileadd(x))

    def test_70_deletefilerecord(self):
        # try to delete the first record

        # find the record to delete, delete it, then validate it's not still in the DB
        record = pathlib.Path(self.AM.all_files()[0].fullpath)
        self.assertTrue(self.AM.filedelete(record) )
        self.assertFalse(self.AM.filefind(record) )


# class MyBackup(backupmanager.BackupManager):

#     def __init__(self, **kwargs):
#         super(MyBackup, self).__init__(**kwargs)

#         self.stopcount = 0

#         self.fileglob = ["*.pyc", "*.dll", "*.csv", "*.iso"]


#     def _dirglob(self):
#         return [] + [self._apath(),]

#     def _drives(self):
#         return [str(pathlib.Path(sys.executable).parent),]

#     def _fileglob(self):
#         return 

#     def _stop(self):
#         # print "test: %s" % self.stopcount
#         self.stopcount += 1
#         if self.stopcount > 8:
#             return True
#         else:
#             return False


# class MyBlankBackup(backupmanager.BackupManager):
#     pass

# class TestBackupManager(unittest.TestCase):

#     def test_10(self):
#         b = MyBackup(mypath=aPATH)
#         b.run()

#     def test_20(self):
#         # test a blank class with nothing in it.
#         b = MyBlankBackup()
#         b.run()


if __name__ == '__main__':
    unittest.main()

