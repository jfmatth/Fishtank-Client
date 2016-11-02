import unittest
import os
import pathlib


import settingsdb

TESTDIR = pathlib.Path(os.path.curdir)

class FirstTest(unittest.TestCase):
    def test1(self):
        # test basic initialization
        c = settingsdb.setting()
        c.initialize(TESTDIR)
        self.assertTrue(c.setup)

if __name__ == "__main__":
    unittest.main()
