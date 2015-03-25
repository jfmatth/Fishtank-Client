import unittest

import Archive
import os
import sys
import pathlib

class TestArchive(unittest.TestCase):

    path = os.environ["TEMP"]
    name = "testarchive.db"

    file = pathlib.Path(sys.argv[0])

    def test_1setUp(self):
        self.archive = Archive.Manager(self.path, name = self.name) 

    def test_2setupOK(self):
        self.assertTrue(os.path.exists(os.path.join(self.path,self.name) ) )
        
    def test_3addfile(self):
        self.assertTrue(self.archive.addfile(self.file) )
        
    def test_4fileinarchive(self):
        self.assertTrue(self.archive.findfile(self.file) )
        
    def test_5listarchives(self):
        x = self.archive.unencrypted_archives()
        x.next()
        x.next()
        x.next()
        x.next()
        x.next()
        
    def test_99tearDown(self):
        self.archive = None
        Archive.close()
        os.remove(os.path.join(self.path, self.name))
    
if __name__ == '__main__':
    unittest.main()