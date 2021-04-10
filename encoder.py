import json
from datetime import datetime

class Serializable():
    def getJSON(self):
        return self.__dict__

class GeneralEncoder(json.JSONEncoder):
    if isinstance(o, Serializable):
        return o.getJSON()
    elif isinstance(o, datetime):
        return o.isoformat()
    else:
        return json.JSONEncoder.default(self, o)