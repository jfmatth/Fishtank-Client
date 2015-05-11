

backup premise
- use Path from pathlib
- start with /Users or %PUBLIC% less one dir (i.e. C:\Users\public -> C:\Users) to start the backup location
- have function for what is to be backed up (both file and dir), similar to what is there now, but not so complicated
- generator of files into Zip?
	- currently it's a generator of zips, but is that better?
	
- make a list of path objects to return?
	once the list is created, return the list and then start feeding them into the zip file in another routine?
	filelistgenerator accounts for files that we don't want to backup and knows about functions for filespec.
	
	filelistgenerator 
		- knows if the filespec is OK
		- knows if the dir is OK
		- knows if the file is in the DB and should be backed up.
		- returns a list of Path objects
	
	for fl in filelistgenerator():
		# fl is a list of files to be backed up.
		
		zip.write(fl.absolute)
		db.update(fl)
		
	- obvious advantages:
		simple design
		if interrupted 



IDEA 2		


	Globals
		ZIPFILE = current zip file we are working on
		FILES = peewee DB		

	FileListGenerator(path):
		for file in path.glob("*"):
			1. Is file excluded in settings
				continue 
				
			2. Is file already in DB (Fall down as they match):
				a. Try to find in DB- Name
				- Date
				- CRC
				continue 
	
			Yield file

	
	AddFileToArchive(file)
		- is there room in the ZIP for another file?
			False = Get new ZIP file to work on. 

		#### SAMPLE PEE WEE CODE
			try:
			    with db.atomic():
			        user = User.create(username=username)
			    return 'Success'
			except peewee.IntegrityError:
			    return 'Failure: %s is already in use.' % username
		###

		try:
			start DB transaction
				- add to zip file
				- update DB with information
		except
			raise (bubble up the error) 		



	MAIN()
		Loop over all drives in system
			for dir in all directories
				if dirOK:
					for file in fileslistgenerator(dir):
						AddFileToArchive(file)
				




	