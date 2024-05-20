#!bin/bash
psql -U postgres -d nameDB -f /docker-entrypoint-initdb.d/migration/V1.0.0_StartingTable.sql
psql -U postgres -d nameDB -f /docker-entrypoint-initdb.d/migration/V1.0.1_CreateRoles.sql
psql -U postgres -d nameDB -f /docker-entrypoint-initdb.d/migration/V1.0.2_AddIndexes.sql
psql -U postgres -d nameDB -f /docker-entrypoint-initdb.d/migration/V1.0.3_Partitioning.sql


#target_version="1.0.2"
#migration_dir="/home/mazastya/DataGrip/migrations/migration/"
#
# Проверка наличия директории с миграциями
#if [ ! -d "$migration_dir" ]; then
#    echo "Директория $migration_dir не существует."
#    exit 1
#fi
#
# Получение списка файлов миграций, отсортированных по версии
#migration_files=$(ls "$migration_dir"/V*.sql | sort -V)
#
# Запуск файлов миграций до указанной версии (включительно)
#for file in $migration_files; do
#    migration_version=$(echo "$file" | sed 's/^.*V\(.*\)_.*$/\1/')
#    if [ "$(printf '%s\n' "$migration_version" "$target_version" | sort -V | head -n1)" = "$migration_version" ]; then
#        echo "Запуск миграции $file"
#        psql -U postgres -d nameDB -f "$file"
#    else
#        break
#    fi
#done
#
#
