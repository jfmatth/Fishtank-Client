from db import Setting, dbInit
import json
import logging
import requests

logger = logging.getLogger(__name__)

class DBDict(dict):
    def __init__(self, name="dbdict.db"):
            
        logger.debug("Calling dbinit")
        dbInit(name)
        
        logger.debug("Updating all my items from the DB")
        for s in Setting.select():
            dict.__setitem__(self, s.key,s.value)

        dict.__init__(self)

    def __setitem__(self, k, v):
        '''
        provide logic to see if the DB needs a replace or new item (built into dict already)
        '''
        logger.debug("_setitem_")
        if self.has_key(k):
            # get the object from the DB, and update it.
            r = Setting.get(key=k)
            r.value = v 
        else:
            r = Setting(key=k, value=v) 

        logger.debug("Saving item to DB")
        r.save()

        dict.__setitem__(self, k, v)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v


class RemoteDict(DBDict):
    # this is mainly a behavior class for subclasses that want to override the behavior methods.

    def __init__(self, *args, **kwargs):
        super(RemoteDict, self).__init__(*args, **kwargs)
        
        # once we are initialized, we call Sync to get the latest data up and down.
        self.Sync()

    def _remoteid(self):
        # whatever our remote id is (url, xmlrpc setup, etc
        return None

    def _remoteSyncUp(self, data):
        pass
    
    def _remoteSyncDown(self):
        pass
    
    def Sync(self):
        logger.debug("Sync")
        if self._remoteid():

            # send it up to the remote system
            logger.debug("Calling _remoteSyncup")
            self._remoteSyncUp()

            #pull down anything we need
            logger.debug("Calling _remoteSyncDown") 
            self._remoteSyncDown()
            

class RemoteUrlDict(RemoteDict):
    # This class will sync to the "remoteid" server via json.
    
    def _showsyncerror(self):
        # do we display an error when the remote sync fails.
        return self.get("showsyncerror", True)

    def _remoteid(self):
        return self.get("remoteid", None)

    def _remoteSyncUp(self):
        # push the data to the remote
        try:        
            headers = {'Content-Type': 'application/json'}
            url = self.get("remoteid")
            r = requests.post(url, data=json.dumps(self), headers=headers)
            print("%s" % r.status_code)
        except:
            if self._showsyncerror():
                raise 
        
    def _remoteSyncDown(self):
        # pull it all down from the server
        try:
            url = self.get("remoteid")
            r = requests.get(url)
            self.update(r.json() )
        except:
            if self._showsyncerror():
                raise
