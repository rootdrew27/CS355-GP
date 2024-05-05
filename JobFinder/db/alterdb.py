import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()



cur.execute("""CREATE TABLE job_application (
    user_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES user(id)
        ON DELETE CASCADE ON UPDATE CASCADE
    CONSTRAINT fk_job FOREIGN KEY (job_id)
        REFERENCES job(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);""")

connection.commit()
connection.close()