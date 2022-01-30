import os

telegram_token = os.getenv('TELEGRAM_TOKEN')

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_database = os.getenv('MYSQL_DATABASE')

database_uri = (
    f'mysql+pymysql://{mysql_user}:{mysql_password}'
    f'@{mysql_host}/{mysql_database}'
)

redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 0))

webhook_host = os.getenv('WEBHOOK_HOST')
webhook_path = os.getenv('WEBHOOK_PATH', '/')
webhook_url = f'{webhook_host}{webhook_path}'

webapp_host = os.getenv('WEBAPP_HOST', '0.0.0.0')
webapp_port = int(os.getenv('WEBAPP_PORT', 8000))

log_level = os.getenv('LOG_LEVEL', 'INFO')
tz = os.getenv('TZ', 'Europe/Moscow')


mandatory_settings = [
    telegram_token, mysql_user, mysql_password, mysql_host, mysql_database, redis_host, redis_port, redis_db,
    webhook_host, webhook_path, webapp_host, webapp_port, log_level, tz
]

if any(setting is None for setting in mandatory_settings):
    raise ValueError(f'One or more of mandatory settings is None\n{mandatory_settings}')
