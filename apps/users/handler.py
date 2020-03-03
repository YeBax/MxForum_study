import json
import random
import jwt
from functools import partial
from tornado.web import RequestHandler
from .forms import SmsCodeForm, RegisterForm, LoginForm
from apps.utils.AsyncYunPian import AsyncYunPian
from MxForum.handler import RedisHandler
from .models import User


class LoginHandler(RedisHandler):
    async def post(self):
        re_data = {

        }
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        form = LoginForm.from_json(param)
        if form.validate():
            mobile = form.mobile.data
            password = form.password.data

            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    re_data["non_fields"] = "用户名或密码错误"
                else:
                    # 登录成功
                    # 1.是不是 rest api 只能使用 jwt （不对）
                    # set_cookie
                    # session 实际上是服务器随机生成的一段字符串，保存在服务器上
                    # JWT 本质还是加密技术，直接解密 userid，user，name，密码不要放进去
                    # 生成 json web token
                    from datetime import datetime
                    payload = {
                        "id": user.id,
                        "nick_name": user.nick_name,
                        "exp": datetime.utcnow() # 必须用UTC时间，jwt有内部检测时间，就是UTC时间
                    }
                    token = jwt.encode(payload, self.settings["secret_key"], algorithm="HS256")
                    re_data["id"] = user.id
                    if user.nick_name is not None:
                        re_data["nick_name"] = user.nick_name
                    else:
                        re_data["nick_name"] = user.mobile
                    re_data["token"] = token.decode("utf-8")
            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["mobile"] = "用户不存在"

            self.finish(re_data)

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
