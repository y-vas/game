import sqlite3, os,bpy

class SQL():
    def __init__(self, db):
        super(SQL, self).__init__()
        self.db = os.path.join(os.path.dirname(bpy.data.filepath),"source","data",db+".db")
        if not os.path.exists(self.db):
            open(self.db,"w")
            # self.add_database()

    def execute(self, query):
        db = sqlite3.connect(self.db)
        cursor = db.cursor()
        cursor.execute(query)
        all_rows = cursor.fetchall()
        # db.close()
        return all_rows

    def execute_one(self, query):
        db = sqlite3.connect(self.db)
        cursor = db.cursor()
        cursor.execute(query)
        user1 = cursor.fetchone() #retrieve the first row
        # all_rows = cursor.fetchall()
        # db.close()
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

    def set_db_structure():
        structure = """

        -- all table must have an id

        -- basic tables --
        CREATE TABLE IF NOT EXISTS `structures` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(255) NULL,
        PRIMARY KEY (`id`));

        CREATE TABLE IF NOT EXISTS `vertices` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `x` DOUBLE NULL,
        `y` DOUBLE NULL,
        `z` DOUBLE NULL,
        PRIMARY KEY (`id`));

        CREATE TABLE IF NOT EXISTS `faces` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `verts` TEXT NULL,
        PRIMARY KEY (`id`));

        """;
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

        dat = self.execute_one("SELECT id FROM "+table+" ORDER BY id desc limit 1;")
        return dat[0]
