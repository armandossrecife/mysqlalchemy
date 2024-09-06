import os

my_username = os.environ.get('MYSQL_USERNAME')
my_password = os.environ.get('MYSQL_PASSWORD')

USERNAME=my_username
PASSWORD=my_password
HOST='localhost'
PORT='3306'
DATABASE_NAME='mydbteste'

mysql_database_url = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"