from decimal import Decimal
from datetime import datetime
import dateutil.parser

class Loyalty():
    def __init__(self,
                 points,         # type: Decimal
                 validUntil=None # type: datetime
                 ):
        self.points = points
        self.validUntil = validUntil

    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Loyalty

        result = cls(**json_dict) 
        result.validUntil = dateutil.parser.parse(json_dict['validUntil'])
        return result