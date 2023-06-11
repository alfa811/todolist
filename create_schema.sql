drop table if exists users ;
drop table if exists todos ;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
    );
-- CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    date DATE, 
    todo TEXT, 
    done BOOLEAN,
    user_id INTEGER, 
    FOREIGN KEY (user_id) REFERENCES users(id));


UPDATE todos SET done = 1 WHERE id = 1