#!/bin/bash

container="mariadb"
sqlfile="fakedata.sql"
volname="openshift_mysqlvolume"

echo "NOTE: mysqlvolume should be recreated before executing this"

docker cp $sqlfile $container:/tmp

docker exec -it $container bash -c "mysql -u sdidbp -p sdidb < /tmp/$sqlfile"

