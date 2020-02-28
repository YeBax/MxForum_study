settings = {
    "redis": {
        "host": "127.0.0.1"
    }
}

import peewee_async
database = peewee_async.MySQLDatabase(
    host='test_db',
    port=3306,
    user="bioinfo",
    password="laso_bioinfo",
    database="webserver",
)