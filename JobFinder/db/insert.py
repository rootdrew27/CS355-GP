import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Researcher', 'Do researching. The Researcher also does a lot of other things, mainly things that allow me to write a longer sequence of characters because I need to test something on the frontend right now. Hopefully it works.', '../static/images/researcher.jpg', 3)")

connection.commit()
connection.close()

