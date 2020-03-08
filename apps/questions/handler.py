from tornado.web import RequestHandler, authenticated
from MxForum.handler import RedisHandler


class GroupHandler(RedisHandler):
    @authenticated
    async def get(self):
        pass
