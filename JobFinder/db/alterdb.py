import sqlite3
import hashlib

# connect to the database 
connection = sqlite3.connect('./JobFinder/db/database.db')

cur = connection.cursor()

# cur.execute(f"""
#     UPDATE user 
#     SET permission_level = 2 WHERE email = 'rootydrew@gmail.com';
# """)


# cur.execute("INSERT INTO department (title, descrip, website_url, email, admin_id) VALUES ('Business', 'The department for Business Stuff is proud to be offering you these words, as these words fill up much space on the page. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'http://fakeurl2.com', 'business@uwec.edu', 4 );") 

connection.commit()
connection.close()

