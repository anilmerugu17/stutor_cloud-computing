# db.py
import os
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        # Anil_local
        # conn = pymysql.connect(user='dbadmin', password='root',
        #                        host='localhost', db='stutor_db')
        # Shiva_local
        conn = pymysql.connect(user='root', password='root',
                               host='localhost', db='Mysql')
    return conn
