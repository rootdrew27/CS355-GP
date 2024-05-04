DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS job;

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    first_n TEXT NOT NULL,
    last_n TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    permission_level INT NOT NULL DEFAULT 0
);

CREATE TABLE department (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    descrip TEXT NOT NULL,
    website_url TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE job (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date_listed NUMERIC NOT NULL DEFAULT (date('now', 'localtime')),
    descrip TEXT NOT NULL,
    img_path TEXT,
    user_id INTEGER,
    dept_id INTEGER,
    CONSTRAINT fk_user FOREIGN KEY (user_id)  --the user that posted the job 
        REFERENCES user(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_department FOREIGN KEY (dept_id)
        REFERENCES department(id)
        ON DELETE CASCADE ON UPDATE CASCADE  
);

-- TODO
-- Create table to 

