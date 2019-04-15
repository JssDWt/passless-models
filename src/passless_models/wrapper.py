from datetime import datetime
import dateutil.parser
import simplejson 

from .receipt import Receipt
from .jsonable import Jsonable

def default_ser(obj):
    if hasattr(obj, 'jsonable'):
        return obj.jsonable()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return simplejson.dumps(obj, sort_keys=True)

class Wrapper(Jsonable):
    def __init__(self,
                 version, # type: str
                 receipt, # type: Receipt
                 ):
        assert isinstance(version, str), "parameter should be str type"
        assert isinstance(receipt, Receipt)
        self.version = version
        self.receipt = receipt

    def to_json(self):
        # type: () -> str
        return simplejson.dumps(self, sort_keys=True, default=default_ser)

    @classmethod
    def from_json(cls, json_str):
        # type: (str) -> Wrapper
        json_dict = simplejson.loads(json_str, use_decimal=True)
        return cls.from_json_dict(json_dict)
    
    @classmethod
    def from_json_dict(cls, json_dict):
        return cls(
            version=json_dict["version"],
            receipt=Receipt.from_json_dict(json_dict["receipt"])
        )