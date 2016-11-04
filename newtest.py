import unittest
import os
import pathlib

import configmanager

TESTDIR = pathlib.Path(os.path.curdir).resolve()
TESTFILE = TESTDIR / "db.json"

class FirstTest(unittest.TestCase):
    c = None

    def setUp(self):
        if os.path.exists(str(TESTFILE)):
            os.remove(str(TESTFILE))

    def test1(self):
        # testing blank initilization
        c = configmanager.ConfigManager()
        c.initialize(TESTDIR)
        c.db.close()

        self.assertTrue(c.setup)


    def test2(self):
        # test initilization and then create with same path.

        c = configmanager.ConfigManager()
        c.initialize(TESTDIR)
        c.db.close()
        self.assertTrue(c.setup)

        c = configmanager.ConfigManager(TESTDIR)
        c.db.close()
        self.assertTrue(c.setup)

    def test3(self):
        # test initializing it, and making sure the test file is where we expect it to be

        c = configmanager.ConfigManager()
        c.initialize(TESTDIR)
        c.db.close()
        self.assertTrue(c.setup)
        self.assertEqual(c.dbpath,TESTDIR)
        
    

if __name__ == "__main__":
    unittest.main()
