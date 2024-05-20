#!/bin/bash

# Параметры из переменных окружения
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-educateForEvery}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-postgres}"
BACKUP_DIR="${BACKUP_DIR:-/home/mazastya/DataGrip/Backups}"
BACKUP_INTERVAL="${BACKUP_INTERVAL:-1}"
KEEP_BACKUPS="${KEEP_BACKUPS:-5}"

backup_db() {
    backup_file="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    PGPASSWORD="$DB_PASS" pg_dumpall -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"  > "$backup_file"
    echo "Backup created: $backup_file"
}

cleanup_backups() {
    cd "$BACKUP_DIR" || exit
    backups=(*.sql)
    backup_count=${#backups[@]}

    if [ "$backup_count" -gt "$KEEP_BACKUPS" ]; then
        num_to_delete=$((backup_count - KEEP_BACKUPS))
        old_backups=($(ls -t *.sql | tail -n "$num_to_delete"))

        for backup in "${old_backups[@]}"; do
            rm "$backup"
            echo "Deleted old backup: $backup"
        done
    fi
}

while true; do
    backup_db
    cleanup_backups
    sleep "$((BACKUP_INTERVAL * 3600))"
done
