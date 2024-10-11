#!/bin/sh
# wait-for-it.sh

set -e

host="$1"
shift
cmd="$@"

until MYSQL_PWD=$MYSQL_PASSWORD mysql -h "$host" -u "$MYSQL_USER" -e 'SELECT 1'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd