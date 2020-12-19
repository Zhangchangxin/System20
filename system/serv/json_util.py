

from datetime import datetime, date
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def json_dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)


def json_loads(s):
    return json.loads(s)
