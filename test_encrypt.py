import unittest

import config

class TestEncryptManager(unittest.TestCase):
    pass

    # def test_CreateNormal(self):
    #     x = config.ConfigManager()
    #     self.assertNotEqual(x.Platform(),None)

    # def test_CreateOverride(self):
    #     x = config.ConfigManager("Windows")
    #     self.assertNotEqual(x.Platform(),None)
    #     self.assertEqual(x.defaultsfile, "defaultwindows.json")

    # def test_CreateBogus(self):
    #     self.assertRaises(Exception, config.ConfigManager, "Bogus" )


# class TestConfigManagerProperties(unittest.TestCase):
#     def setUp(self):
#         self.config = config.ConfigManager()

#     def test_ArchivePath(self):
#         self.assertNotEqual(self.config.ArchivePath, None)

#     def test_RootFolders(self):
#         self.assertNotEqual(self.config.RootFolders(), None)

#     def test_maxsizekb(self):
#         self.assertGreater(self.config.maxfilesizekb,0)

#     def test_publickey(self):
#         self.assertIsNotNone(self.config.publickey)

#     def test_cryptextension(self):
#         self.assertIsNotNone(self.config.cryptextension)
        
#     def test_BogusProperty(self):
#         with self.assertRaises(Exception):
#             self.config.bogusproperty
    

if __name__ == '__main__':
    unittest.main()