import unittest
import os

import configmanager

class TestConfigManager(unittest.TestCase):
    
    def setUp(self):
        if os.path.exists(configmanager.ConfigManager.DBNAME): 
            os.remove(configmanager.ConfigManager.DBNAME)

    def test_10_create(self):
        # basic creation
        c = configmanager.ConfigManager(".")            
    
    def test_20_saveattributes(self):
        # start with a fresh configmanager, add the urlpath, delete the object, reinstanciate, make sure it's the same

        PATH = "http://somepath"

        c = configmanager.ConfigManager(".")
        self.assertIsNone(c.urlpath)
        c.urlpath = PATH
        del(c)
        c = configmanager.ConfigManager(".")
        self.assertEqual(c.urlpath, PATH)

    def test_21_dontsaveattribute(self):
        c = configmanager.ConfigManager(".")
        c.badattribute = "this wont be saved"
        del(c)
        c = configmanager.ConfigManager(".")
        if hasattr(c,"badattribute"):
            raise Exception("attribute should not be here")
        
    def test_30_savesettings(self):
        # save some settings
        c = configmanager.ConfigManager(".")
        c.settings["key1"] = "value1"
        c.settings["key2"] = 3
        c.settings["key3"] = {"dict1":1, "dict2":2}

    def test_40_saveandgetsettings(self):
        # save some settings, delete the object, create a new one, bring back the settings. 
        c = configmanager.ConfigManager(".")
        c.settings["key1"] = "value1"
        c.settings["key2"] = 3
        c.settings["key3"] = {"dict1":1, "dict2":2}
        del(c)
        c = configmanager.ConfigManager(".")
        self.assertEqual(c.settings["key1"], "value1")
        self.assertEqual(c.settings["key2"], 3)
        self.assertEqual(c.settings["key3"], {"dict1":1, "dict2":2})
        
if __name__ == '__main__':
    unittest.main()
