import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./db/database.db')

# execute table creation 
# with open('./db/schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()
# cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Steve', 'Thestudent', 'Steve@gmail.com', '{hashlib.md5('password'.encode())}', 1)")
# cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Suzy', 'Theteacher', 'Suzy@gmail.com', '{hashlib.md5('password'.encode())}', 2)")
# cur.execute(f"INSERT INTO department (title, descrip) VALUES ('Computer Science', 'A department for computer stuff')")
# cur.execute(f"INSERT INTO job (title, descrip, user_id, dept_id) VALUES ('Programmer', 'Write Programs', 2, 1)")
# cur.execute(f"INSERT INTO job (title, descrip, user_id) VALUES ('Cafeteria Worker', 'Serve soup', 2)")
# cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Suzy', 'Theteacher', 'Suzy@gmail.com', '{hashlib.md5('password'.encode())}', 2)")
cur.execute(f"INSERT INTO job (title, descrip, user_id) VALUES ('Salesman', 'Sell my stuff', 2)")
cur.execute(f"INSERT INTO job (title, descrip, user_id) VALUES ('Salesman', 'Sell my stuff', 2)")

connection.commit()
connection.close()

