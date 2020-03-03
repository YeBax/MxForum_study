from tornado.web import url
from .handler import SmsHandler, RegisterHandler, LoginHandler
url_pattern = (
    url("/code/", SmsHandler),
    url("/register/", RegisterHandler),
    url("/login/", LoginHandler),

)