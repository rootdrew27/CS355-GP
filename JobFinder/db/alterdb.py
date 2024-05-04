import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()

cur.execute("""ALTER TABLE user ADD COLUMN path_to_r_file text;""")

cur.execute("""ALTER TABLE user ADD COLUMN path_to_t_file text;""")

connection.commit()
connection.close()