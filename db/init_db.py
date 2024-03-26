import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('database.db')

# execute table creation 
# this will fail if the table has already been created
with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
cur.execute(f"INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Steve', 'Thestudent', 'Steve@gmail.com', '{hashlib.md5('password'.encode())}' 1)")


# INSERT INTO user (first_n, last_n, permission_level) VALUES ('Suzy', 'Theteacher', 2);
# INSERT INTO department (title, descrip) VALUES ('Computer Science', 'A department for computer stuff');
# INSERT INTO job (title, descrip, user_id, dept_id) VALUES ('Programmer', 'Write Programs', 2, 1);

connection.commit()
connection.close()




##### EXAMPLE INSERTIONS ######

# cur = connection.cursor()
# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('First Post', 'Content for the first post')
#             )

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )