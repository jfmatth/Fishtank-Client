# all of our DB stuff goes into this file.

import peewee
from peewee import CompositeKey

from environment import settings

# database = peewee.SqliteDatabase("sqlite3.db")
database = peewee.SqliteDatabase(settings["db"]["path"])

class basetable(peewee.Model):

    class Meta:
        database = database

# Setting - basically a key / value DB
class Setting(basetable):
    key = peewee.CharField(unique=True)
    value = peewee.TextField(null=True)


# # Backup - represents a ZIP file backup
# class Backup(basetable):
#     fullpath = peewee.CharField(unique=True, index=True)
#     ready     = peewee.BooleanField(index=True)
#     encrypted = peewee.BooleanField(index=True)
#     uploaded  = peewee.BooleanField(index=True)
#
#
# # File - each file in the ZIP, related to that parent record.
# class File(basetable):
#     backup   = peewee.ForeignKeyField(Backup)
#
#     fullpath = peewee.CharField(index=True)
#     crc      = peewee.CharField(index=True)
#     filename = peewee.CharField()
#     size     = peewee.IntegerField()
#     modified = peewee.DateField()
#     accessed = peewee.DateField()
#     created  = peewee.DateField()
#
#     class Meta:
#         primary_key = CompositeKey("fullpath", "crc")


database.connect()
database.create_tables([Setting], safe=True)
# database.create_tables([Backup],  safe=True)
# database.create_tables([File],    safe=True)

#
#
#
# # Initialize all the tables
# def dbInit(name="database.db"):
#     database.init(name)
#     database.connect()
#     database.create_tables([Setting], safe=True)
#     database.create_tables([Backup], safe=True)
#     database.create_tables([File], safe=True)
