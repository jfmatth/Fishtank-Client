import peewee
import logging

logger = logging.getLogger(__name__)

"""
DB Layout

Backup
    |
    |--> File
"""

# Define the DB's we'll use in this module.
database = peewee.SqliteDatabase(None)
class basetable(peewee.Model):
    class Meta:
       database = database

# Backup - represents a ZIP file backup
class Backup(basetable):
    fullpath = peewee.CharField(unique=True, index=True)
    ready = peewee.BooleanField(index=True)
    encrypted = peewee.BooleanField(index=True)
    uploaded = peewee.BooleanField(index=True)

# File - each file in the ZIP, related to that parent record.
class File(basetable):
    backup = peewee.ForeignKeyField(Backup)

    fullpath = peewee.CharField(index=True)
    crc = peewee.CharField(index=True)
    filename = peewee.CharField()
    size = peewee.IntegerField()
    modified = peewee.DateField()
    accessed = peewee.DateField()
    created = peewee.DateField()

    class Meta:
        primary_key = peewee.CompositeKey("fullpath", "crc")
