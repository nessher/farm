#!/bin/bash
set -e
umask 077
DIR=/root/backups
DATE=$(date +%F_%H%M)
docker exec postgres_db pg_dump -U postgres_admin postgres_database | gzip > $DIR/db_$DATE.sql.gz
tar -czf $DIR/media_$DATE.tar.gz -C /root/farm media
# хранить 14 дней
find $DIR -type f -mtime +14 -delete
