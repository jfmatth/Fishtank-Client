import unittest

import archive
import os
import sys
import pathlib
import uuid

p = os.environ['TEMP']
f = pathlib.Path(sys.argv[0])


class TestArchive(unittest.TestCase):
    
    def test_1_checkall(self):
        a = archive.ArchiveManager(p, "test.db")
        
        # validate they all exist
        for z in a.all_archives():
            self.assertTrue(os.path.exists(z.fullpath))
         
        a.close()

    def test_closearchive(self):

        a = archive.ArchiveManager(p, "test.db")

        a.close()
        
        # check that all the settings are reset    
        self.assertEqual(a.size, 0, "Size check not 0")
        self.assertEqual(a.archive, None, "Archive not None")
        self.assertEqual(a.name, None, "Name not blank")


    def test_2_deleteall(self):
        a = archive.ArchiveManager(p, "test.db")

        for z in a.all_archives():
            self.assertTrue( a.delete_archive(z.fullpath), z.fullpath )
             
        a.close()
           
    def test_3sizelimit(self):
        # generate some random files to be added to the archive.
        JUNKLINE = "abcedfdfasf;laksjf;lasdfjalsfjas;ldfkjwl;erjioweurj3434udsfjasf;lkjsafpoierhihioshdaf;asjflkasjf\n"
        def junk(filename):
            with open(filename,"w") as f:
                for l in xrange(1,1000):
                    f.write(JUNKLINE)
   
   
        a = archive.ArchiveManager(p, "test.db")

        a.limit = 1024 * 1000
   
        for x in xrange(1,10):
            JUNKFILE = str(uuid.uuid4() )
            jpath = pathlib.Path(p) / JUNKFILE
            fx = pathlib.Path("%s.txt" % (jpath) )
            junk(fx.as_posix())
            a.addfile(fx)
            os.remove(fx.as_posix() )
    
        a.close()


if __name__ == '__main__':
    unittest.main()

