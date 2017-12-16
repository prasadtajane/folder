README

### To set up:
```
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```
### To create the db and associated tables and begin running the mysql server
If you have mysql installed globally on your machine run:
```
$ ./db_create
```
Otherwise, navigate to the /bin directory under your XAMPP installation and run:
```
$ mysql.server restart
$ mysql -u root < /path/to/trainly/directory/database/create_db.sql
```


### To clear the DB and populate it with the data from init_db.sql
/nIf you have mysql installed globally on your run:
```
$ ./db_fill
```
Otherwise, navigate to the /bin directory under your XAMPP installation and run:
```
$ mysql.server restart
$ mysql -u root < /path/to/trainly/directory/database/init_db.sql
```

### To run the flask application run:
```
$ ./run
```

### To create the DB, start the server, fill it with the sample data and start the web app (if you have mysql globally)
```
$ ./db_init_run
```

### To stop sql server
If you have mysql installed globally on your machine:
```
$ ./db_stop
```
Otherwise, navigate to the /bin directory under your XAMPP installation and run:
```
$ mysql.server stop
```

### To get out of the virtualenv:
```
$ deactivate
```
