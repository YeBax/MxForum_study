from tornado.web import url
from .handler import GroupHandler
url_pattern = [
    url("/groups/", GroupHandler),

]