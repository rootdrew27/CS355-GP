import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()

cur.execute("""DELETE FROM job WHERE id = 8 OR id = 9""")

##### DELETE roota5351 
# cur.execute("""DELETE FROM user WHERE email = 'roota5351@uwec.edu'""")

# cur.execute("""DELETE FROM job_application WHERE user_id = 6""")

# cur.execute(f"""
#     UPDATE user 
#     SET permission_level = 2 WHERE email = 'rootydrew@gmail.com';
# """)

# cur.execute("""UPDATE user 
#             SET path_to_r_file = NULL
#             WHERE email = 'roota5351@uwec.edu'""")

# cur.execute("""INSERT INTO user (first_n, last_n, email, password, permission_level) VALUES ('Drew', 'Root', 'root.drew27@gmail.com', 'password1', 2)""")

# cur.execute("""INSERT INTO job (title, descrip, img_path, user_id) VALUES ('Python Developer', 'Write amazing code in python. Its better than Java.', './static/images/pythonDev.png', 7)""")
# cur.execute("""UPDATE job
#             SET dept_id = 2
#             WHERE title = 'Writer' or title = 'Salesman'""")
# cur.execute("""UPDATE job
#             SET dept_id = 1
#             WHERE title = 'Hacker'""")

# cur.execute("INSERT INTO department (title, descrip, website_url, email, admin_id) VALUES ('Business', 'The department for Business Stuff is proud to be offering you these words, as these words fill up much space on the page. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'http://fakeurl2.com', 'business@uwec.edu', 4 );") 

connection.commit()
connection.close()

