settings = {
    "redis": {
        "host": "127.0.0.1"
    },
    "secret_key":"SFSAF$#%$%ADFSDF#RD",
    "jwt_expire":7*24*3600
}

import peewee_async
database = peewee_async.MySQLDatabase(
    host='test_db',
    port=3306,
    user="bioinfo",
    password="laso_bioinfo",
    database="webserver",
)

