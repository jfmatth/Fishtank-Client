import unittest
import os
import pathlib

import settingsdb

TESTDIR = pathlib.Path(os.path.curdir).resolve()
TESTFILE = TESTDIR / "db.json"

class FirstTest(unittest.TestCase):
    c = None

    def setUp(self):
        os.remove(str(TESTFILE))

    def test1(self):
        # testing blank initilization
        c = settingsdb.setting()
        c.initialize(TESTDIR)

        self.assertTrue(c.setup)

        c.db.close()

    def test2(self):
        # test initilization and then create with same path.

        c = settingsdb.setting()
        c.initialize(TESTDIR)
        self.assertTrue(c.setup)
        c.db.close()

        c = settingsdb.setting(TESTDIR)
        self.assertTrue(c.setup)

        c.db.close()


    def test3(self):
        c = settingsdb.setting()
        c.initialize(TESTDIR)
        c.db.close()
        self.assertTrue(c.setup)

        self.assertEqual(c.dbfile,TESTFILE)
        
        c.db.close()
        

    



if __name__ == "__main__":
    unittest.main()
