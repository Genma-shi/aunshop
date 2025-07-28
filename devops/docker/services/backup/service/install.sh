#!/bin/sh

set -eu

BACKUP_FILE=/opt/services/backup_service/service/backup.sh

notification_service() {
    local MESSAGE="$1"

    local JSON_DATE="{\"content\":\"$MESSAGE\"}"

    curl -H "Content-Type: application/json" -d "$JSON_DATE" "${WEBHOOK_URL}"
}

if [ -z "$SCHEDULE" ]; then
  sh $BACKUP_FILE
else
  notification_service "Ежедневный бэкап сервиса ${PROJECT_NAME} установлен"
  exec go-cron "$SCHEDULE" sh $BACKUP_FILE || notification_service "Произошла ошибка в установке бэкап сервиса"
fi
