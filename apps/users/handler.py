import json
import random
from functools import partial
from tornado.web import RequestHandler
from .forms import SmsCodeForm, RegisterForm
from apps.utils.AsyncYunPian import AsyncYunPian
from MxForum.handler import RedisHandler
from .models import User


class SmsHandler(RedisHandler):
    def generate_code(self):
        """
        生成随机 4位数字的验证码
        :return:
        """
        code_str = []
        for i in range(4):
            code_str.append(str(random.randint(0, 9)))
        return ''.join(code_str)

    async def post(self):
        re_data = {}

        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():
            mobile = sms_form.mobile.data
            code = self.generate_code()
            yun_pain = AsyncYunPian("asdfsafq2123")
            re_json = await yun_pain.send_single_sms(code, mobile)
            # re_json = await partial(yun_pain.send_single_sms, code, mobile)
            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json["msg"]
            else:
                # 成功，将验证码写入到redis中，并设置一个有效时间
                # self.redis_conn.set("{}_{}".format(mobile, code), 1, 10*60)
                print("存入redis")
                re_data["msg"] = "ok"
                re_data["code"] = code
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]

        self.finish(re_data)


class RegisterHandler(RedisHandler):
    async def post(self):
        re_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 验证码 是否正确
            redis_key = "{}_{}".format(mobile, code)
            # if not self.redis_conn.get(redis_key):
            if not 1:
                self.set_status(400)
                re_data["code"] = "验证码错误或者失效"
            else:
                # 验证用户是否存在
                try:
                    existed_user = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已经存在"
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data["id"] = user.id
                    re_data["msg"] = "创建成功"

        else:
            self.set_status(400)
            for field in register_form.erros:
                re_data[field] = register_form[field][0]

        self.finish(re_data)
