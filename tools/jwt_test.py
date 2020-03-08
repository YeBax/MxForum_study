from datetime import datetime
import jwt

current_time = datetime.utcnow()

data = jwt.encode({
    "name": "bax",
    "id": 1,
    "exp": current_time,
}, "aaa").decode("utf-8")

import time

time.sleep(3)

send_data = jwt.decode(data, "aaa", leeway=1, options={
    "verify_exp": False
})

print(send_data)
