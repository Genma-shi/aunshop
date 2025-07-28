from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    default_acl = 'public-read'  # <-- Делает каждый файл публичным
    file_overwrite = False       # <-- Одинаковые имена — разные файлы
