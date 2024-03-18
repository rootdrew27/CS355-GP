import sqlite3
import datetime

connection = sqlite3.connect('database.db')

cur = connection.cursor()

# print(cur.execute("SELECT * FROM sqlite_master where type='table';").fetchall())


cur.execute("INSERT INTO jobs (title, job_description) VALUES (?, ?)",
            ('Teacher', 'Teach Students')
            )

# cur.execute("INSERT INTO jobs (title, job_description) VALUES (?, ?)",
#             ('Programmer', 'Write code')
#             )


connection.commit()
connection.close()