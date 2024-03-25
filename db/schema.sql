CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date_listed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    job_description TEXT NOT NULL
)

-- additionally, jobs needs a foreign key to User, to allow a poster to be attached to the job
-- and a fk for a department