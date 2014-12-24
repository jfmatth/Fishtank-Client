import unittest
import os

from settingsdict import SettingsDict
from db import dbInit as Init

TESTFILE = "tests.db"

class SimpleSettings_Basics(unittest.TestCase):
    '''
    Test the settings module.
    
    Store a pair of keys 
    '''
    k1 = "Key1"
    k2 = "Key2"
    
    v1 = 'Value 1'
    v2 = 'Value 2'

    def test_0setUp(self):
        try:
            os.remove(TESTFILE)
        except:
            pass
        Init(TESTFILE)
        
    def test_1Add(self):
        c = SettingsDict("tests.db")
        c[self.k1] = self.v1
        c[self.k2] = self.v2
        
    def test_2Recall(self):
        c = SettingsDict("tests.db")
        self.assertEqual(c[self.k1], self.v1)
        self.assertEqual(c[self.k2], self.v2)
        
    def test_3Overwrite(self):
        c = SettingsDict("tests.db")
        c[self.k1] = self.v1
        self.assertIn(self.k1, c)
        
    def test_4totalitems(self):
        c = SettingsDict("tests.db")
        self.assertTrue(len(c)==2)

if __name__ == '__main__':
    unittest.main()

