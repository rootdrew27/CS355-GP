import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./db/database.db')

cur = connection.cursor()
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Hacker', 'Hack peoples stuff.', '../static/images/hacker.jpg', 2)")

connection.close()

