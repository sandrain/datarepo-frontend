#!/bin/bash

container="sdidb"
sqlfile="fakedata.sql"

echo "NOTE: mysqlvolume should be recreated before executing this"

docker cp $sqlfile $container:/tmp

#docker exec -it $container bash -c "mysql -u sdidbp -p sdidb < /tmp/$sqlfile"
docker exec -it $container bash -c "psql -U sdidbp -d sdidb -f /tmp/$sqlfile"

