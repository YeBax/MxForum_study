from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

MOBILE_REGEX = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"


class SmsCodeForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入正确的手机号码")])


class RegisterForm(Form):
    mobile = StringField("手机号码", validators=[
        DataRequired(message="请输入手机号码"),
        Regexp(MOBILE_REGEX, message="请输入正确的手机号码")])
    code = StringField("验证码", validators=[DataRequired(message="验证码不能为空")])
    password = StringField("密码", validators=[DataRequired(message="请输入密码"), Length(max=20, min=6)])

