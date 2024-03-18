import sqlite3

# connect to the database 
connection = sqlite3.connect('database.db')

# execute table creation 
# this will fail if the table has already been created!!
with open('schema.sql') as f:
    connection.executescript(f.read())

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