import unittest
import os
import sys
import pathlib

from import archivemanager
import backupmanager

aPATH = pathlib.Path("archives/").resolve()

class TestaManager(unittest.TestCase):

    def test_20_fileadd(self):
        a = a.aManager(aPATH)
        f = pathlib.Path(sys.executable)

        self.assertTrue(a.fileadd(f))

        # adding the same file should also return true, even though it's not added.
        self.assertTrue(a.fileadd(f))

    def test_30_filefind(self):
        a = a.aManager(aPATH)
        f = pathlib.Path(sys.executable)

        self.assertTrue(a.filefind(f) )

    def test_40_checkas(self):

        a = a.aManager(aPATH)

        for f in a.all_as():
            self.assertTrue( str(os.path.exists(f.fullpath)) )

    def test_60_addallpython(self):

        p = pathlib.Path(sys.executable).parent
        a = a.aManager(aPATH)

        # add all files in the python directory
        for x in p.glob("*"):
            if not x.is_dir():
                self.assertTrue(a.fileadd(x))

    def test_70_deletefilerecord(self):
        # try to delete the first record
        a = a.aManager(aPATH)

        # find the record to delete, delete it, then validate it's not still in the DB
        record = pathlib.Path(a.all_files()[0].fullpath)
        self.assertTrue(a.filedelete(record) )
        self.assertFalse(a.filefind(record) )



class MyBackup(backupmanager.BackupManager):

    def __init__(self, **kwargs):
        super(MyBackup, self).__init__(**kwargs)

        self.stopcount = 0

        self.fileglob = ["*.pyc", "*.dll", "*.csv", "*.iso"]


    def _dirglob(self):
        return [] + [self._apath(),]

    def _drives(self):
        return [str(pathlib.Path(sys.executable).parent),]

    def _fileglob(self):
        return 

    def _stop(self):
        # print "test: %s" % self.stopcount
        self.stopcount += 1
        if self.stopcount > 8:
            return True
        else:
            return False


class MyBlankBackup(backupmanager.BackupManager):
    pass

class TestBackupManager(unittest.TestCase):

    def test_10(self):
        b = MyBackup(mypath=aPATH)
        b.run()

    def test_20(self):
        # test a blank class with nothing in it.
        b = MyBlankBackup()
        b.run()


if __name__ == '__main__':
    unittest.main()

