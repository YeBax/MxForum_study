import json
import tornado.ioloop
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from urllib.parse import urlencode


class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        http_client = httpclient.AsyncHTTPClient()
        url = "http://www.baidu.com"
        text = "aaa:{}".format(code)
        b = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        }
        post_request = HTTPRequest(url=url, method="POST", body=urlencode(b))
        res = await http_client.fetch(post_request)
        # return json.loads(res.body.decode("utf-8"))
        return {
            "code": 0,
            "msg": "ok"
        }


if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    yun_pian = AsyncYunPian("akfjsjf123jldjf")

    from functools import partial

    new_func = partial(yun_pian.send_single_sms, "1234")
    io_loop.run_sync(new_func)
