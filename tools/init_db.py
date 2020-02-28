from apps.users.models import User
from peewee import MySQLDatabase

database = MySQLDatabase(
    host='test_db',
    port=3306,
    user="bioinfo",
    password="laso_bioinfo",
    database="webserver",
)


def init():
    database.create_table(User)


if __name__ == '__main__':
    init()
