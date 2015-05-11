import peewee
from peewee import CompositeKey

database = peewee.SqliteDatabase(None)

class basetable(peewee.Model):
    class Meta:
        database = database

# Setting - basically a key / value DB
class Setting(basetable):
    key = peewee.CharField(unique=True)
    value = peewee.TextField(null=True)

    def All(self):
        return self.select()


# Backup - represents a ZIP file backup
class Backup(basetable):
    fullpath = peewee.CharField(unique=True, index=True)
    encrypted = peewee.BooleanField(index=True)             # encrypted zips are called?
    uploaded = peewee.BooleanField(index=True)

    def All(self):
        return self.select()


# File - each file in the ZIP, related to that parent record.
class File(basetable):
    archive =  peewee.ForeignKeyField(Backup)
    
    fullpath = peewee.CharField(index=True)
    crc      = peewee.CharField(index=True)
    filename = peewee.CharField()
    size     = peewee.IntegerField()
    modified = peewee.DateField()
    accessed = peewee.DateField()
    created  = peewee.DateField()
    
    class Meta:
        primary_key = CompositeKey("fullpath", "crc")


# Initialize all the tables
def dbInit(name="database.xdb"):
    database.init(name)
    database.connect()
    database.create_tables([Setting], safe=True)
    database.create_tables([Backup], safe=True)
    database.create_tables([File], safe=True)
