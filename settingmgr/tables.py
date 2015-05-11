import peewee
import argparse

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


def dbInit(name="database.xdb"):
    database.init(name)
    database.connect()
    database.create_tables([Setting], safe=True)

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
