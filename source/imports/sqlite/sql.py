import bpy, os, sys

filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
sqli = os.path.join(directory, "Scripts", "Imports", "sqlite","sqlite3.h")

if sqli not in sys.path:
   sys.path.append(sqli)

import sqlite3

class SQL():
    def __init__(self, db):
        super(SQL, self).__init__()
        self.db = os.path.join(directory,db+".db")
        if not os.path.exists(self.db):
            open(self.db,"w")
            # self.add_database()

    def execute(self, query):
        db = sqlite3.connect(self.db)
        cursor = db.cursor()
        cursor.execute(query)
        # user1 = cursor.fetchone() #retrieve the first row
        all_rows = cursor.fetchall()
        db.close()
        return all_rows

    def execute_one(self, query):
        db = sqlite3.connect(self.db)
        cursor = db.cursor()
        cursor.execute(query)
        user1 = cursor.fetchone() #retrieve the first row
        # all_rows = cursor.fetchall()
        db.close()
        return user1

    def insert(self, query):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        try:
          c.execute(query)
        except sqlite3.IntegrityError as e:
          print('sqlite error: ', e.args[0])
        conn.commit()
        pass

    def insert_and_get_last_serial(self, query):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        ins = query.split(" ")
        try:
          c.execute(query)
        except sqlite3.IntegrityError as e:
          print('sqlite error: ', e.args[0])
        conn.commit()

        table ="";
        for i,value in enumerate(ins):
            if value == "INTO" or value == "into":
                table = ins[i+1]
                break

        dat = self.execute_one("SELECT COUNT(*) FROM "+table+" ;")
        return dat[0]
