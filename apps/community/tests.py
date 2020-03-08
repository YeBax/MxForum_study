import requests

from datetime import datetime
import jwt
from MxForum.settings import settings

current_time = datetime.utcnow()

data = jwt.encode({
    "name": "bax",
    "id": 1,
    "exp": current_time,
}, settings["secret_key"]).decode("utf8")

print(data)

requests.get("http://127.0.0.1:8888/groups/", headers={
    "tsessionid": data
})
