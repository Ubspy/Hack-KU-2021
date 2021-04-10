import json

class Serializable():
    def getJSON(self):
        return self.__dict__

class GeneralEncoder(JSONEncoder):
    if isinstance(o, MedicalSerializable):
        return o.getJSON()
    elif isinstance(o, datetime):
        return o.isoformat()
    else:
        return json.JSONEncoder.default(self, o)