import peewee
import argparse

db = peewee.SqliteDatabase(None)

class basetable(peewee.Model):
    class Meta:
        database = db

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
    backup   = peewee.ForeignKeyField(Backup, related_name='files')

    fullpath = peewee.CharField(unique=True, index=True)
    crc      = peewee.CharField(index=True)
    filename = peewee.CharField()
    size     = peewee.IntegerField()
    modified = peewee.DateField()
    accessed = peewee.DateField()
    created  = peewee.DateField()






def dbInit(name="database.db"):
    db.init(name)
    db.connect()
    db.create_tables([Setting], safe=True)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--init", help="Initialize the database", action="store_true")
    parser.add_argument("-N", "--name", help="Name of DB" )
    args = parser.parse_args()

    if args.init:
        print("Initalizing Database")
        if args.name:
            dbInit(args.name)
        else:    
            dbInit()
