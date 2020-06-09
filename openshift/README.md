## To test on your local machine ##

Istall docker and docker-compose and then:

```
$ cd docker-test
15:06:33 hyogi@veronica docker-test $ docker-compose build
mariadb uses an image, skipping
Building sdifrontend
Step 1/6 : FROM centos/python-36-centos7
 ---> 2394c24793aa
Step 2/6 : WORKDIR /code
 ---> Using cache
 ---> 8d1269d2dd23
Step 3/6 : COPY requirements.txt /code/
 ---> Using cache
 ---> 23413d1d338f
Step 4/6 : RUN pip install --upgrade pip
 ---> Using cache
 ---> f833fb7a227e
Step 5/6 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 771b6770ab64
Step 6/6 : COPY docker-test /code/
 ---> 9ba008f779f3
Successfully built 9ba008f779f3
Successfully tagged docker-test_sdifrontend:latest
15:06:38 hyogi@veronica docker-test $ docker-compose up
Creating mariadb ... done
Creating sdifrontend ... done
Attaching to mariadb, sdifrontend

 ... (omitted) ...

mariadb        | 2020-03-24 19:08:30 139644342126272 [Note] Added new Master_info '' to hash table
mariadb        | 2020-03-24 19:08:30 139644342126272 [Note] mysqld: ready for connections.
mariadb        | Version: '10.2.31-MariaDB-1:10.2.31+maria~bionic'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
sdifrontend    | Connected to database:  [('sdidb',)]
sdifrontend    | Database is up - executing command
sdifrontend    | Performing system checks...
sdifrontend    |
sdifrontend    | System check identified no issues (0 silenced).
sdifrontend    |
sdifrontend    | You have 14 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, mainpage, sessions.
sdifrontend    | Run 'python manage.py migrate' to apply them.
sdifrontend    | March 24, 2020 - 19:08:33
sdifrontend    | Django version 1.11.29, using settings 'sdifrontend.settings'
sdifrontend    | Starting development server at http://0.0.0.0:8000/
sdifrontend    | Quit the server with CONTROL-C.
```

Try http://localhost:8000/ in your browser.

To execute commands in the context of a container:

```
hyogi@veronica docker-test $ docker container ls
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                              NAMES
bbcfba3914df        docker-test_sdifrontend   "container-entrypoin…"   3 minutes ago       Up 3 minutes        0.0.0.0:8000->8000/tcp, 8080/tcp   sdifrontend
b34e45d97cf9        mariadb:10.2              "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        0.0.0.0:3306->3306/tcp             mariadb
hyogi@veronica docker-test $ docker exec sdifrontend /code/manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, mainpage, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying mainpage.0001_initial... OK
  Applying sessions.0001_initial... OK
hyogi@veronica docker-test $
```

It is also possible to directly access the containers. For instance, to access
the django container (named `sdifrontend` in the `docker-compose.yml` file):

```
hyogi@veronica docker-test $ docker exec -it sdifrontend bash
(app-root) bash-4.2$ ls
conf        dbtest       mainpage   openshift  requirements.txt
db.sqlite3  docker-test  manage.py  README.md  sdifrontend
(app-root) bash-4.2$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, mainpage, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying mainpage.0001_initial... OK
  Applying sessions.0001_initial... OK
(app-root) bash-4.2$ exit
exit
hyogi@veronica docker-test $
```

Similarly, for accessing the mariadb container:

```
hyogi@veronica docker-test $ docker exec -it mariadb bash
root@b34e45d97cf9:/# mysql -uroot -p
Enter password:
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 13
Server version: 10.2.31-MariaDB-1:10.2.31+maria~bionic mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sdidb              |
+--------------------+
4 rows in set (0.00 sec)

MariaDB [(none)]> use sdidb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [sdidb]> show tables;
+----------------------------+
| Tables_in_sdidb            |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| auth_user                  |
| auth_user_groups           |
| auth_user_user_permissions |
| django_admin_log           |
| django_content_type        |
| django_migrations          |
| django_session             |
| mainpage_dataset           |
+----------------------------+
11 rows in set (0.00 sec)

MariaDB [sdidb]> exit
Bye
root@b34e45d97cf9:/# exit
exit
hyogi@veronica docker-test $
```

The mariadb container creates a persistent volume file:

```
hyogi@veronica docker-test $ ls -l
total 20
-rw-r--r-- 1 hyogi hyogi  163 Mar 24 12:31 Dockerfile
-rw-r--r-- 1 hyogi hyogi 3561 Mar 24 14:58 README.md
drwxr-xr-x 2 hyogi hyogi 4096 Mar 24 14:52 container-scripts/
-rw-r--r-- 1 hyogi hyogi 1039 Mar 24 12:30 docker-compose.yml
drwxr-xr-x 5 saned root  4096 Mar 24 14:51 mysqldb/
hyogi@veronica docker-test $
```

Do not manually edit files in the `mysqldb/` directory. When the database needs
to be wiped out completely:

```
hyogi@veronica docker-test $ sudo rm -rf mysqldb
```

Also, to remove current containers to rebuild new ones:

```
hyogi@veronica docker-test $ docker-compose rm -fv
Going to remove sdifrontend, mariadb
Removing sdifrontend ... done
Removing mariadb     ... done

# then you can rebuild the containers
hyogi@veronica docker-test $ docker-compose build
# and launch the services
hyogi@veronica docker-test $ docker-compose up
```


