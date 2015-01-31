import logging
import re
import os

import zlib
import stat
import time
import json
import zipfile
import re
import uuid


from dbdict import DBDict
from conf import constants

logger = logging.getLogger(__name__)
settings = DBDict(constants.SETTING_FILE)

_shutdown = False

def shutdown(event):
    logger.info("Received shutdown event..")
    _shutdown = True

class BackupSpec():
    def __init__(self, fs=None, ds=None):
        self.filespec = fs
        self.dirspec = ds
        
        self.fileregex = re.compile(self.filespec or "", re.IGNORECASE)
        self.dirregex = re.compile(self.dirspec or "", re.IGNORECASE)
                
    def dirok(self, dirname=None):
        """
        if dirname is a match to our regex, the return FALSE, otherwise return TRUE.  Sort of 
        unintuitive, but directories that match won't be backed up.
        """
        if not dirname==None:
            if self.dirregex.match(dirname):
                return False
            else:
                logger.debug("checking %s" % dirname)
                return True
        else:
            return False
        
    def fileok(self, filename=None):
        """
        Same as directories, don't backup matching patterns 
        """
        if not filename==None:
            # split out the filename
            if self.fileregex.match( os.path.split(filename)[1] ):
                return False
            else:
                return True
        else:
            return False
        
    def __repr__(self):
        return "filespec=%s, dirspec=%s, dirspec=%s" % (self.filespec, self.dirspec, self.dirspec)




def crcval(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)




def fileinfo(filename):
    """ returns a dict of all the file information we want of a file """
    fi = {}
    fs = os.stat(filename)

    fi['crc']      = crcval(filename)
    fi['filename'] = filename
    fi['size']     = fs[stat.ST_SIZE]
    fi['modified'] = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(fs[stat.ST_MTIME]))
    fi['accessed'] = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(fs[stat.ST_ATIME]))
    fi['created']  = time.strftime("%m/%d/%Y %I:%M:%S %p",time.localtime(fs[stat.ST_CTIME]))
    
    return fi


def ZipDBFile(path):
    """ Return a unique pair for zip and db filenames, prefixed with the path """
    tempname = str( uuid.uuid4() )

    zipfilename = os.path.join(path, tempname + ".backup")
    dbfilename  = os.path.join(path, tempname + ".db")

    return zipfilename, dbfilename



def BackupGenerator(spec = None,
                    temppath = None,
                    datapath = None,
                    drives   = None,
                    limit    = 100,
                    stopbackup = None,
                    ):
    """ A generators that returns two filenames:
        zipfile, dbfile. zipfile is a zip of all files that should be backed up because the CRC changed, or it wasn't 
        in the fulldb.dbm database.  dbfile is a DBM of the zipfile files
        
        filespec - which files to backup (*.txt), but as a python regular expression.
        temppath - Where to put the temporary files (zip and db)
        datapath - where does the dbfull.db live?
        drives   - the outer loop of which locations to backup (C:/, d:/, etc), can be folder qualification too.
        limit    - how big in MB should each (pre compressed) backup set be before yielding. backed up
    """
   
    if (spec == None or temppath == None or datapath == None or drives == None):
        raise Exception("invalid values for Backup")

    if not type(drives)==list:
        raise Exception("drives must be of type list") 

    logger.debug("temppath = %s" % temppath)
    logger.debug("datapath = %s" % datapath)
    logger.debug("drives = %s" % drives)

    maxfilecount = 10000

    try:
        fulldbname = os.path.join(datapath, "dbfull.db")
        
        # change how we use limit, have the calling user set it correctly in actual bytes.
        #_limit = limit * 1024 * 1024
        _limit = limit
        logger.debug("filesize = %s" % _limit)
        _size = 0 
        _zip    = None
        _dbdiff = None
        _dbfull = anydbm.open(fulldbname, "c")
        
        # define our filenames as blanks, so we can see them?
        zf = None
        dbf = None
    
        _count = 0
        
        # define a variable to stop us backing up, cause the runbackup() could be "expensive"
        stoprunning = False
    
        logger.debug("Starting loop over drives")
        
        for drive in drives:
        
            currdir = os.path.normpath(drive)
                
            logger.debug("currdir %s in drives" % currdir)
                
            if len(currdir) != 0:
                
                for root, dirs, files in os.walk(currdir):
                    
                    if stopbackup():
                        logger.debug("raise StopIteration")
                        raise StopIteration

                    # if this directory shouldn't be 'walked' then move on
                    if not spec.dirok(root):
                        continue

                    logger.debug("backup: size = %s, count=%s" % (_size, _count) )
                    
                    for f in files:
                        fullpath = os.path.normcase(os.path.normpath(os.path.join(root,f) ) ) 

                        if os.path.isfile(fullpath) and spec.fileok(fullpath):
                            try:
                                finfo = fileinfo(fullpath)
                                
                                # filesize max check
                                if int(finfo['size']) > _limit:
                                    logger.debug("file %s too big, skipping" % fullpath)
                                    continue 

                                if not _dbfull.has_key(fullpath) or not json.loads(_dbfull[fullpath])['crc'] == finfo['crc']:
                                    # it's not in our DB or it's different, then update the DB and the zip
                                    
                                    if _zip == None:
                                        # we need a zip and DBM opened, cause they may have been closed
                                        # when we generated back.
                                        zf, dbf = ZipDBFile(temppath)
                                        _zip    = zipfile.ZipFile(zf, "w", compression=zipfile.ZIP_DEFLATED)
                                        _dbdiff = anydbm.open(dbf, "n")

                                    sfinfo = json.dumps(finfo)                            
                                    _zip.write(fullpath)
                                    _dbdiff[fullpath] = sfinfo
                                    _count += 1

                                    _size  += finfo['size']

                                    # check for stop 'zipping' condition.
                                    if (_size >= _limit or _count >= maxfilecount):
                                        logger.debug("Size: %s, len(_dbdiff) = %s " % (_size, len(_dbdiff) ) )
                                        _zip.close()
                                        _dbdiff.close()
                                        _zip = None
                                        _dbdiff = None
                                        _size = 0
                                        _count = 0
                                        yield zf, dbf
    
                            except Exception as e:
                                logger.critical("%s Exception on %s" % (e, fullpath) )
     
        logger.debug("Done looping over drives")

        if stoprunning:
            logger.debug("Stoprunning signal received")
            
        # once we have traversed everything, clean up the last of it all.                                
        if not _zip == None:
            # still here
            logger.info("len(_dbdiff) = %s " % len(_dbdiff) )
            _zip.close()
            _dbdiff.close()
            _zip = None
            _dbdiff = None
            _dbfull.close()
            _dbfull = None

            yield zf, dbf
    
    except StopIteration:
        # something stopped us, so clean up.
        if not _zip == None:
            _zip.close()
            _dbdiff.close()
            _zip = None
            _dbdiff = None
            logger.debug("Erase dbf %s" % dbf)
            os.remove(dbf)
            logger.debug("Erase zip %s" % zf)
            os.remove(zf)
            _size = 0
            _count = 0
    
    except:
        logger.exception("Error in BackupGenerator")





def backupmain(cloud = None):
    
    if cloud == None:
        logger.exception("no cloud to backup to")
        raise Exception("No cloud to backup to :) ")
    
    logger.info("BackupToCloud() starting")

#     # Ping the server first, to make sure we can see if this is worth while.
#     ping_host = settings[".managerhost"]
#     ping_guid = settings[".guid"]
#     if not utility.server_ping(host=ping_host, guid=ping_guid):
#         logger.debug("Tracker Offline, returning")
#         return

    insdir = settings['.installdir']

    filespec = settings["filespec"]
    if filespec == None:
        raise("Can't have a blank filespec")
    logger.info("filespec = %s" % filespec)
    
    if settings["temppath"] == None:
        raise("No temppath specified")
    temppath = os.path.normpath(insdir + settings['temppath'])
    utility.check_dir(temppath)
    logger.info("temppath = %s" % temppath)
    
    if settings["dbpath"] == None:
        raise("no DB path specified")
    dbpath = os.path.normpath(insdir + settings['dbpath'])
    utility.check_dir(dbpath)
    logger.info("dbpath = %s" % dbpath)
    
    drives = utility.LogicalDrives()
    logger.info("drives = %s" % drives)

    # put the calculation here for the full backup size, default is 100 MB
    backupsize = settings["backupsize"] or 100
    backupsize = int(backupsize) * 1024 * 1024
        
### this needs to be moved into the generator portion of the code
    # check to see how much free space we have, and if we have enough to backup anything?
    size, free = utility.diskspaceinfo(os.path.splitdrive(settings[".installdir"])[0] )
    if free <= backupsize * 2  :
        logger.info("no room for backup, sorry")
        logger.debug("freespace = %s, backupsize = %s" % (free, backupsize))
        return
###

    # define new BackupSpec varaiable that we can pass in to check for dirs and files to backup.
    installdir = settings['.installdir'].replace("\\", "\\\\").lower()
    dirspec = settings['dirspec'] + '|' + installdir
    backupspec = BackupSpec(fs=filespec, ds=dirspec)
    logger.debug("backupspec = %s" % backupspec)
    
    pk = settings[".publickey"]
    
    if settings["cloud_files"] == None:
        raise("no cloud_files specified")
    cloudpath = os.path.normpath(insdir + settings['cloud_files'])
    utility.check_dir(cloudpath)

    logger.info("Starting backup loop")

    # define them here, since we need to check them at close
    _dbfull = None
    _dbdiff = None
    
    if _shutdown:
        logger.debug("_shutdown True")
        return
    
    # we get backup 'sets' in sizes of limit in each loop
    # once we get a generated pair (zf=zipfile, dbf=database of files in zip), we encrypt and upload to tracker.
    for zf, dbf in backup.BackupGenerator(backupspec, temppath, dbpath, drives, limit=backupsize, stopbackup=stopfunc):

        # we should be able to modularize this better, but it is somewhat critical section, 
        # if any of the items below are interrupted, then the backup will be incomplete.


        # The new model just needs to update the DB with the new zip file and save it, then move on
        # the encryption and upload will be done by another module / job.
        pass 

#         try:
#             logger.debug("zf = %s\n dbf = %s" % (zf, dbf) )
#     
#             filein  = zf
#             fileout = os.path.join(cloudpath,os.path.basename(zf) + "-e") 
#         
#             key = str(uuid.uuid4() )[:32]
# 
#             logger.info("Encrypting %s"  % filein)
# #            encrypt.EncryptAFile(filein=filein, fileout=fileout, key=key)
#             # replace with new PyCrypto version.
#             encrypt.encrypt_file(key=key,
#                                  in_filename=filein,
#                                  out_filename=fileout)
#     
#             # file is encrypted, sitting at fileout.
#             # encrypt the key and push to server?
#             ekey = encrypt.EncryptAString(key, pk)[0]
#             rawfilename = os.path.basename(dbf)
#             host = settings[".managerhost"]
#             url = "/manager/dbmupload/"
#             fields = [("eKey",urllib.quote(ekey)),
#                       ("clientguid", settings[".guid"]),
#                       ("backupguid", rawfilename.split(".")[0]),
#                  ]
#             files = [("dFile",rawfilename,open(dbf,"rb").read() )]
# 
#             # now upload the DBF for the tracker for keeping track of all files backed up.        
#             logger.info("Uploading %s" % dbf)
#             status, reason, data = upload.httppost_multipart(host, url, fields, files)
#             logger.debug("status = %s" % status)
#             logger.debug("reason = %s" % reason)
# 
#             if status == 200:
#                 # so the file is encrypted and uploaded, now put it in the cloud.
#                 logger.debug("Adding to cloud")
#                 cloud.put(fileout)
#         
#                 # now, update the dbfull database to show that the files are updated.
#                 logger.debug("Updating dbfull.db")
#                 if _dbfull == None:
#                     # only open if we need to.
#                     _dbfull = anydbm.open(os.path.join(dbpath, "dbfull.db"), "c") 
#                 _dbdiff = anydbm.open(dbf)
#                 for key in _dbdiff:
#                     # if it's not there, or the CRC's are different, update the DBfull db.
#                     if ( not _dbfull.has_key(key) ) or ( not json.loads(_dbfull[key])['crc'] == json.loads(_dbdiff[key])['crc'] ): 
#                         _dbfull[key] = _dbdiff[key]
#                 _dbdiff.close()
#                 logger.debug("dbfull.db updated")
#             else:
#                 logger.critical("Failed to upload DB for backup, canceling backup")
#                 break
#             
#             if os.path.exists(dbf):
#                 if not _dbdiff == None: _dbdiff = None
#                 logger.debug("erasing %s" % dbf)
#                 os.remove(dbf)
#     
#             if os.path.exists(zf):
#                 logger.debug("erasing %s" % zf)
#                 os.remove(zf)
# 
#             # free disk space check (Again)
#             size, free = utility.diskspaceinfo(os.path.splitdrive(settings[".installdir"])[0] )
#             if free <= backupsize * 2 :
#                 logger.info("no room for backup, sorry")
#                 logger.debug("freespace = %s, backupsize = %s" % (free, backupsize))
#                 break                
# 
#             logger.debug("Continuing")
#                 
#         except:
#             logger.exception("Exception after Backup Generation")
#             raise
# 
#     if not _dbfull == None:
#         logger.debug("closing dbfull")
#         _dbfull.close()
#     if not _dbdiff == None:
#         logger.debug("closing & removing dbdiff(%s)" % dbf)
#         _dbdiff.close()
#         os.remove(dbf)
    
    logger.info("BackupToCloud() finished")
    


    
if __name__ == "__main__":
    backupmain()
