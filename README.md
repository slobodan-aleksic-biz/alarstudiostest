# alarstudiostest

# I task

1. Create dockerdile and docker-composer.yml for the flask project
    a. create an image according to requirements.txt
    b. install postgres
    c. install pgAdmin
    d. set an env variable for a posgres DB and use it in the project

2. Create the users table in the DB with the id, name, username, password and is_admin fields
3. Create a DB with script create_db.py and feed the DB table users
3. Make simple CRUD for the User model using JQuery Ajax as expresed by the task requirements

## Steps to run the project

### Open a terminal
1. docker-compose build
2. docker-compose up

### Open second terminal and type in:
3. docker-compose exec app bash
4. python app/create_db.py

### You can access the project at
http://localhost:5000/

### You can log in with username: slobodan and password: secret

# II task
### The path for the second task
http://localhost:5000/async_get