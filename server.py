from tornado import web
import tornado.ioloop
from peewee_async import Manager
from MxForum.urls import url_pattern
from MxForum.settings import settings, database

if __name__ == '__main__':
    # 集成json 到wtforms
    import wtforms_json

    wtforms_json.init()

    app = web.Application(url_pattern, debug=True, **settings)
    app.listen(8888)

    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    tornado.ioloop.IOLoop.current().start()
