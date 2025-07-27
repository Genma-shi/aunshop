#! /bin/sh

set -e

DATE=$(date +"%Y-%m-%d")
YEAR=$(date +"%Y")
MONTH=$(date +"%m")
DAY=$(date +"%d")
S3=${S3_URL}/databases/${BACKUP_DIR}/${YEAR}/${MONTH}/${DAY}/

check_storage_directory() {
    if [ -z "$(ls -A ${BACKUP_DIR})" ]; then
        mkdir -p ${BACKUP_DIR}
    fi
}

notification_service() {
    local MESSAGE="$1"

    local JSON_DATE="{\"content\":\"$MESSAGE\"}"

    curl -H "Content-Type: application/json" -d "$JSON_DATE" "${WEBHOOK_URL}"
}

creating_backup(){
    local FILE_FORMAT=$1
    local BACKUP_FILE=$2

    PGPASSWORD=${POSTGRES_PASSWORD} pg_dump --format=${FILE_FORMAT} \
            -h ${POSTGRES_HOST} \
            -p ${POSTGRES_PORT} \
            -U ${POSTGRES_USER} \
            -d ${POSTGRES_DB} \
            > ${BACKUP_FILE} || notification_service "Ошибка создания бэкапа командой pg_dump"
}

get_and_upload_backup(){
    echo "Creating backup of $POSTGRES_DATABASE database..."
    local SQL_BACKUP="${BACKUP_DIR}/${DATE}_${PROJECT_NAME}.sql"
    local DUMP_BACKUP="${BACKUP_DIR}/${DATE}_${PROJECT_NAME}.dump"

    creating_backup plain ${SQL_BACKUP}

    creating_backup custom ${DUMP_BACKUP}

    upload_to_cloud "${SQL_BACKUP}"

    upload_to_cloud "${DUMP_BACKUP}"
}

upload_to_cloud(){
    local FILE=$1

    s3cmd put $FILE $S3 || notification_service "Что-то пошло не так при загрузке бэкапа проекта ${PROJECT_NAME}."

    if [ $? -eq 0 ]; then
        notification_service "Бэкап для проекта ${PROJECT_NAME} успешно загружен в AWS ($(date +"%Y-%m-%d %H:%M:%S")). Файл: ${FILE}"
    else
        notification_service "Ошибка в загрузке бэкапа."
    fi
}

check_storage_directory

get_and_upload_backup
