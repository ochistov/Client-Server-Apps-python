from datetime import datetime

TIME = datetime.now().replace(microsecond=0).isoformat(sep=' ')

ENCODING = 'UTF-8'

RESPONSE = {
    "response": None,
    "time": str(TIME),
    "alert": None
}

PRESENCE = {
    "action": "presence",
    "time": str(TIME),
    "type": "status",
    "user": {
        "account_name": "GUEST"
    }
}

MESSAGE = {
    "action": "msg",
    "time": str(TIME),
    "message": None
}

SERVER_RESPONSE = (
    ('200', 'OK'),
    ('401', 'Not authorized'),
    ('404', 'Not found')
)
