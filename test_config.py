import unittest

from config import cfg

class TestConfigManagerCreate(unittest.TestCase):

    def test_CreateNormal(self):
        self.assertNotEqual(cfg.Platform(),None)

    def test_CreateOverride(self):
        self.assertNotEqual(cfg.Platform(),None)
        self.assertEqual(cfg.defaultsfile, "defaultwindows.json")

    # def test_CreateBogus(self):
    #     self.assertRaises(Exception, config.ConfigManager, "Bogus" )


class TestConfigManagerProperties(unittest.TestCase):
    # def setUp(self):
    #     self.config = config.ConfigManager()

    def test_ArchivePath(self):
        self.assertNotEqual(cfg.ArchivePath, None)

    def test_RootFolders(self):
        self.assertNotEqual(cfg.RootFolders(), None)

    def test_maxsizekb(self):
        self.assertGreater(cfg.maxfilesizekb,0)

    def test_publickey(self):
        self.assertIsNotNone(cfg.publickey)

    def test_cryptextension(self):
        self.assertIsNotNone(cfg.cryptextension)
        
    def test_BogusProperty(self):
        with self.assertRaises(Exception):
            cfg.bogusproperty
    

if __name__ == '__main__':
    unittest.main()