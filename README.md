### Setting Dictionary (seetingdict)

A subclass of dict that saves things in a local sqlite DB and/or a remote server  

Requirements
```
peewee ORM 2.4.*
requests 2.4.*
```
				
Sample usage
```
from settingsdict import SettingsDict
s = SettingsDict()

s['a'] = 1234
s['b'] = 2345

print s
{u'a': u'1234', u'b': u'2345'} 

del(s)
s = SettingsDict()
print s
{u'a': u'1234', u'b': u'2345'} 
```

SettingDict takes an optional name argument.  Name is the name of the database you want to create.


Also, there is RemoteUrlDict which provides with sync up / down methods.

Using the 'remoteid' key, it will attempt to POST a json copy of itself up to the 'remoteid' value, and sync down via a GET from the same 'remoteid'


```
u = RemoteUrlDict()
u['remoteid'] = "http://127.0.0.1:8080/settings"
u['value'] = "this is a test value"
u.Sync()
```

Here is the sample Bottle.py code used for testing
```
from bottle import route, request, run, response
import json

@route('/settings', method='POST')
def writedata():

    try:
        print request.json
    except:
        pass
  
@route("/settings", method="GET")
def readdata():
    testdata = {'id' : "34dfdjfier", 'name':'blah blah blah'}
    response.content_type = "application/json"
    return json.dumps(testdata)
    
run(host='localhost', port=8080) 
```
