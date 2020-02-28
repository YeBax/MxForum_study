from tornado.web import url
from .handler import SmsHandler, RegisterHandler
url_pattern = (
    url("/code/", SmsHandler),
    url("/register/", RegisterHandler),
)