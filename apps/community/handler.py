# from tornado.web import authenticated
from MxForum.handler import RedisHandler
from apps.utils.mxform_decoratiors import authenticated_async


class GroupHandler(RedisHandler):
    # @authenticated_async
    # async def get(self):
    #     tsessionid = self.request.headers.get("tsessionid", None)
    #     pass

    @authenticated_async
    async def post(self):
        re_data = {}

