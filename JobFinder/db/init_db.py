import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

# execute table creation 
with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Steve', 'Thestudent', 'Steve@gmail.com', 'password', 1)")
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Suzy', 'Theteacher', 'Suzy@gmail.com', 'password', 2)")
cur.execute(f"INSERT INTO department (title, descrip, website_url, email) VALUES ('Learning & Technology Services', 'LTS provides the campus community with instructional and informational technology tools as well as a robust networking infrastructure and the support to foster all aspects of student learning and academic excellence.', 'https://www.uwec.edu/lts', 'helpdesk@uwec.edu')")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id, dept_id) VALUES ('Programmer', 'Write Programs', 'c', 2, 1)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Janitor', 'Perform a variety of cleaning tasks.', '../static/images/janitor.jpg', 2)")
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Sally', 'Theotherteacher', 'Sally@gmail.com', 'password', 2)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Salesman', 'Sell my stuff.', '../static/images/salesman.jpg', 2)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Writer', 'Write beautiful things.', '../static/images/writer.jpg', 2)")
cur.execute(f"INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Hacker', 'Hack peoples stuff. The Hacker also does a lot of other things, mainly things that allow me to write a longer sequence of characters because I need to test something on the frontend right now. Hopefully it works.', '../static/images/hacker.jpg', 2)")

connection.commit()
connection.close()

