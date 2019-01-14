from decimal import Decimal

class Payment():
    # TODO: Add different kinds of payment?
    def __init__(self,
                 method,   # type: str
                 amount,   # type: Decimal
                 meta=None # type: dict
                 ):
        self.method = method
        self.amount = amount
        self.meta = meta
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Payment

        return cls(**json_dict)