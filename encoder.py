import json
from datetime import datetime, date

class Serializable():
    def getJSON(self):
        return self.__dict__

class GeneralEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Serializable):
            return o.getJSON()
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)