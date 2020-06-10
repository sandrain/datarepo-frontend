#!/bin/bash

container="postgresql"
sqlfile="fakedata.sql"

docker cp $sqlfile $container:/tmp

docker exec -it $container bash -c "psql -U sdidbp -d sdidb -f /tmp/$sqlfile"

