import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./db/database.db')

# execute table creation 
with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Steve', 'Thestudent', 'Steve@gmail.com', 'password', 1)")
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Suzy', 'Theteacher', 'Suzy@gmail.com', 'password', 2)")
cur.execute(f"INSERT INTO department (title, descrip) VALUES ('Computer Science', 'A department for computer stuff')")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id, dept_id) VALUES ('Programmer', 'Write Programs', 'c', 2, 1)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Janitor', 'Perform a variety of cleaning tasks.', '../static/images/janitor.jpg', 2)")
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Sally', 'Theotherteacher', 'Sally@gmail.com', 'password', 2)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Salesman', 'Sell my stuff.', '../static/images/salesman.jpg', 2)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Writer', 'Write beautiful things.', '../static/images/writer.jpg', 2)")

connection.commit()
connection.close()

