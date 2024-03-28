import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./db/database.db')

cur = connection.cursor()

print(cur.execute(f"Select first_n from user WHERE email='Steve@gmail.com'").fetchall()[0][0])



