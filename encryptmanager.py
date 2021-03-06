# find all files that are encrypted but not uploaded yet, and upload

import logging
import os
import pathlib


from config import ConfigManager
from archivemanager import ArchiveManager

logger = logging.getLogger(__name__)

def EncryptFile(filein, fileout, key):
    """
    
    """
    assert isinstance(filein, pathlib.Path)
    assert isinstance(fileout, pathlib.Path)

    print(filein, fileout, key)

class EncryptManager(object):
    """
    Encypts file that aren't already encrypted - Dah.
    """
    def __init__(self)
        logger.debug("EncryptManager: __init__")

        self.config = ConfigManager()
        self.am = ArchiveManager(self.config)

    def run(self):
        """
        find all archives that need to be encrypted and encrypt them.
        """
        logger.debug("EncryptManager: run()")

        pk = self.config.publickey
        outext = self.config.cryptextension

        for a in self.am.unencrypted_archives():
            try:
                EncryptFile(a.fullpath, a.pullpath, pk)
                a.encrypted = True
                a.save()
            except:
                logger.exception("failed to encrypt the file")




# 			fileout = os.path.join(cloudpath,os.path.basename(zf) + "-e") 
		
# 			key = str(uuid.uuid4() )[:32]

# 			log.info("Encrypting %s"  % filein)
# #			encrypt.EncryptAFile(filein=filein, fileout=fileout, key=key)
# 			# replace with new PyCrypto version.
# 			encrypt.encrypt_file(key=key,
# 								 in_filename=filein,
# 								 out_filename=fileout)
	
# 			# file is encrypted, sitting at fileout.
# 			# encrypt the key and push to server?
# 			ekey = encrypt.EncryptAString(key, pk)[0]
# 			rawfilename = os.path.basename(dbf)
# 			host = settings[".managerhost"]
# 			url = "/manager/dbmupload/"
# 			fields = [("eKey",urllib.quote(ekey)),
# 					  ("clientguid", settings[".guid"]),
# 				      ("backupguid", rawfilename.split(".")[0]),
# 				 ]
# 			files = [("dFile",rawfilename,open(dbf,"rb").read() )]

# 			# now upload the DBF for the tracker for keeping track of all files backed up.		
# 			log.info("Uploading %s" % dbf)
# 			status, reason, data = upload.httppost_multipart(host, url, fields, files)
# 			log.debug("status = %s" % status)
# 			log.debug("reason = %s" % reason)








# def BackupFromCloud( cloud = None, 
# 					 settings = None 
# 					):
	
# 	if cloud == None:
# 		raise Exception("No cloud to backup to :) ")
	
# 	if settings == None:
# 		raise Exception("No Settings to use :)")
	
# 	log.debug("BackupFromCloud() Starting.")

# 	# Ping the server first, to make sure we can see if this is worth while.
# 	ping_host = settings[".managerhost"]
# 	ping_guid = settings[".guid"]

# 	if not utility.server_ping(host=ping_host, guid=ping_guid):
# 		log.debug("Tracker Offline, returning ")
# 		return

# 	# get the size and free space on this drive. 
# 	size, free = utility.diskspaceinfo(os.path.splitdrive(settings[".installdir"])[0] )

# 	# how much space are we taking up?
# 	clouddir = os.path.normpath(os.path.join(settings['.installdir'], settings['cloud_files']) )
# 	cloudspace = utility.pathspaceinfo(clouddir)

# 	# we will ask for a torrent of size < = amount then.
# 	managerhost = settings[".managerhost"]
# 	guid = settings[".guid"]
# 	HTTPConnection = httplib.HTTPConnection(managerhost)
# 	parms = urllib.urlencode( {'guid': guid, 'size': size, 'cloud': cloudspace, 'free':free} )
# 	URL = "/manager/diskspace/"

# 	HTTPConnection.request("POST", URL, parms)
# 	response = HTTPConnection.getresponse()

# 	if response.status != 200:
# 		log.debug("error : URL: %s msg:%s txt:%s" % (URL, response.reason, response.read() ) )
# 	else:
# 		infohash = response.read()
# 		if len(infohash) > 0:
# 			# get it from the cloud()
# 			log.info("Asing for hash %s" % infohash)
# 			cloud.get(infohash)

# 	log.debug("BackupFromCloud() finished")


# class BackupSpec():
# 	def __init__(self, fs=None, ds=None):
# 		self.filespec = fs
# 		self.dirspec = ds
		
# 		self.fileregex = re.compile(self.filespec or "", re.IGNORECASE)
# #		self.dirlist = self.dirspec.split("|")
# 		self.dirregex = re.compile(self.dirspec or "", re.IGNORECASE)
				
# 	def dirok(self, dirname=None):
# 		"""
# 		if dirname is a match to our regex, the return FALSE, otherwise return TRUE.  Sort of 
# 		unintuitive, but directories that match won't be backed up.
# 		"""
# 		if not dirname==None:
# 			if self.dirregex.match(dirname):
# 				return False
# 			else:
# 				log.debug("checking %s" % dirname)
# 				return True
# 		else:
# 			return False
		
# 	def fileok(self, filename=None):
# 		"""
# 		Same as directories, don't backup matching patterns 
# 		"""
# 		if not filename==None:
# 			# split out the filename
# 			if self.fileregex.match( os.path.split(filename)[1] ):
# 				return False
# 			else:
# 				return True
# 		else:
# 			return False
		
# 	def __repr__(self):
# 		return "filespec=%s, dirspec=%s, dirspec=%s" % (self.filespec, self.dirspec, self.dirspec)


# def BackupToCloud(	cloud = None, 
# 					settings = None, 
# 					stopfunc=None
# 				):
	
# 	if cloud == None:
# 		log.exception("no cloud to backup to")
# 		raise Exception("No cloud to backup to :) ")
	
# 	if settings == None:
# 		log.exception("No settings passed in")
# 		raise Exception("No Settings to use :)")
	
# 	if not hasattr(stopfunc, '__call__'):
# 		log.exception("no stopfunc defined")
# 		raise Exception("no stopfunc defined")
	
# 	log.info("BackupToCloud() starting")

# 	# Ping the server first, to make sure we can see if this is worth while.
# 	ping_host = settings[".managerhost"]
# 	ping_guid = settings[".guid"]

# 	if not utility.server_ping(host=ping_host, guid=ping_guid):
# 		log.debug("Tracker Offline, returning")
# 		return

# 	insdir = settings['.installdir']

# 	filespec = settings["filespec"]
# 	if filespec == None:
# 		raise("Can't have a blank filespec")
# 	log.info("filespec = %s" % filespec)
	
# 	if settings["temppath"] == None:
# 		raise("No temppath specified")
# 	temppath = os.path.normpath(insdir + settings['temppath'])
# 	utility.check_dir(temppath)
# 	log.info("temppath = %s" % temppath)
	
# 	if settings["dbpath"] == None:
# 		raise("no DB path specified")
# 	dbpath = os.path.normpath(insdir + settings['dbpath'])
# 	utility.check_dir(dbpath)
# 	log.info("dbpath = %s" % dbpath)
	
# 	drives = utility.LogicalDrives()
# 	log.info("drives = %s" % drives)

# 	# put the calculation here for the full backup size, default is 100 MB
# 	backupsize = settings["backupsize"] or 100
# 	backupsize = int(backupsize) * 1024 * 1024
		
# ### this needs to be moved into the generator portion of the code
# 	# check to see how much free space we have, and if we have enough to backup anything?
# 	size, free = utility.diskspaceinfo(os.path.splitdrive(settings[".installdir"])[0] )
# 	if free <= backupsize * 2  :
# 		log.info("no room for backup, sorry")
# 		log.debug("freespace = %s, backupsize = %s" % (free, backupsize))
# 		return
# ###

# 	# define new BackupSpec varaiable that we can pass in to check for dirs and files to backup.
# 	installdir = settings['.installdir'].replace("\\", "\\\\").lower()
# 	dirspec = settings['dirspec'] + '|' + installdir
# 	backupspec = BackupSpec(fs=filespec, ds=dirspec)
# 	log.debug("backupspec = %s" % backupspec)
	
# 	pk = settings[".publickey"]
	
# 	if settings["cloud_files"] == None:
# 		raise("no cloud_files specified")
# 	cloudpath = os.path.normpath(insdir + settings['cloud_files'])
# 	utility.check_dir(cloudpath)

# 	log.info("Starting backup loop")

# 	# define them here, since we need to check them at close
# 	_dbfull = None
# 	_dbdiff = None
	
# 	if stopfunc():
# 		log.debug("stopfunc returned true, returning from module.")
# 		return
	
# 	# we get backup 'sets' in sizes of limit in each loop
# 	# once we get a generated pair (zf=zipfile, dbf=database of files in zip), we encrypt and upload to tracker.
# 	for zf, dbf in backup.BackupGenerator(backupspec, temppath, dbpath, drives, limit=backupsize, stopbackup=stopfunc):

# 		# we should be able to modularize this better, but it is somewhat critical section, 
# 		# if any of the items below are interrupted, then the backup will be incomplete.

# 		try:
# 			log.debug("zf = %s\n dbf = %s" % (zf, dbf) )
	
# 			filein  = zf
# 			fileout = os.path.join(cloudpath,os.path.basename(zf) + "-e") 
		
# 			key = str(uuid.uuid4() )[:32]

# 			log.info("Encrypting %s"  % filein)
# #			encrypt.EncryptAFile(filein=filein, fileout=fileout, key=key)
# 			# replace with new PyCrypto version.
# 			encrypt.encrypt_file(key=key,
# 								 in_filename=filein,
# 								 out_filename=fileout)
	
# 			# file is encrypted, sitting at fileout.
# 			# encrypt the key and push to server?
# 			ekey = encrypt.EncryptAString(key, pk)[0]
# 			rawfilename = os.path.basename(dbf)
# 			host = settings[".managerhost"]
# 			url = "/manager/dbmupload/"
# 			fields = [("eKey",urllib.quote(ekey)),
# 					  ("clientguid", settings[".guid"]),
# 				      ("backupguid", rawfilename.split(".")[0]),
# 				 ]
# 			files = [("dFile",rawfilename,open(dbf,"rb").read() )]

# 			# now upload the DBF for the tracker for keeping track of all files backed up.		
# 			log.info("Uploading %s" % dbf)
# 			status, reason, data = upload.httppost_multipart(host, url, fields, files)
# 			log.debug("status = %s" % status)
# 			log.debug("reason = %s" % reason)

# 			if status == 200:
# 				# so the file is encrypted and uploaded, now put it in the cloud.
# 				log.debug("Adding to cloud")
# 				cloud.put(fileout)
		
# 				# now, update the dbfull database to show that the files are updated.
# 				log.debug("Updating dbfull.db")
# 				if _dbfull == None:
# 					# only open if we need to.
# 					_dbfull = anydbm.open(os.path.join(dbpath, "dbfull.db"), "c") 
# 				_dbdiff = anydbm.open(dbf)
# 				for key in _dbdiff:
# 					# if it's not there, or the CRC's are different, update the DBfull db.
# 					if ( not _dbfull.has_key(key) ) or ( not json.loads(_dbfull[key])['crc'] == json.loads(_dbdiff[key])['crc'] ): 
# 						_dbfull[key] = _dbdiff[key]
# 				_dbdiff.close()
# 				log.debug("dbfull.db updated")
# 			else:
# 				log.critical("Failed to upload DB for backup, canceling backup")
# 				break
			
# 			if os.path.exists(dbf):
# 				if not _dbdiff == None: _dbdiff = None
# 				log.debug("erasing %s" % dbf)
# 				os.remove(dbf)
	
# 			if os.path.exists(zf):
# 				log.debug("erasing %s" % zf)
# 				os.remove(zf)

# 			# free disk space check (Again)
# 			size, free = utility.diskspaceinfo(os.path.splitdrive(settings[".installdir"])[0] )
# 			if free <= backupsize * 2 :
# 				log.info("no room for backup, sorry")
# 				log.debug("freespace = %s, backupsize = %s" % (free, backupsize))
# 				break				

# 			log.debug("Continuing")
				
# 		except:
# 			log.exception("Exception after Backup Generation")
# 			raise

# 	if not _dbfull == None:
# 		log.debug("closing dbfull")
# 		_dbfull.close()
# 	if not _dbdiff == None:
# 		log.debug("closing & removing dbdiff(%s)" % dbf)
# 		_dbdiff.close()
# 		os.remove(dbf)
	
# 	log.info("BackupToCloud() finished")