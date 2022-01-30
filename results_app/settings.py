import os

mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_host = os.getenv('MYSQL_HOST')
mysql_database = os.getenv('MYSQL_DATABASE')

database_uri = (
    f'mysql+pymysql://{mysql_user}:{mysql_password}'
    f'@{mysql_host}/{mysql_database}'
)

mandatory_settings = [
    mysql_user, mysql_password, mysql_host, mysql_database
]

if any(setting is None for setting in mandatory_settings):
    raise ValueError(f'One or more of mandatory settings is None\n{mandatory_settings}')
