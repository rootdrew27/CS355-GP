DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS job;

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    first_n TEXT NOT NULL,
    last_n TEXT NOT NULL,
    permission_level INT NOT NULL DEFAULT 0
);

CREATE TABLE department (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    descrip TEXT NOT NULL
);

CREATE TABLE job (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date_listed NUMERIC NOT NULL DEFAULT (date('now', 'localtime')),
    descrip TEXT NOT NULL,
    user_id INTEGER,
    dept_id INTEGER,
    CONSTRAINT fk_user FOREIGN KEY (user_id)  --the user that posted the job 
        REFERENCES user(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_department FOREIGN KEY (dept_id)
        REFERENCES department(id)
        ON DELETE CASCADE ON UPDATE CASCADE  
);

-- examples

INSERT INTO user (first_n, last_n, permission_level) VALUES ('Steve', 'Thestudent', 0);
INSERT INTO user (first_n, last_n, permission_level) VALUES ('Suzy', 'Theteacher', 1);
INSERT INTO department (title, descrip) VALUES ('Computer Science', 'A department for computer stuff');
INSERT INTO job (title, descrip, user_id, dept_id) VALUES ('Programmer', 'Write Programs', 2, 1);