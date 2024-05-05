import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()

cur.execute("""ALTER TABLE department ADD COLUMN email text;""")

connection.commit()
connection.close()