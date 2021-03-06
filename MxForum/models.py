from peewee import *
from peewee import Model
import datetime
from .settings import database



class BaseModel(Model):
    add_time = DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        database = database
