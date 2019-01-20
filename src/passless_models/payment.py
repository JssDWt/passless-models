from decimal import Decimal

class Payment():
    # TODO: Add different kinds of payment?
    def __init__(self,
                 method,   # type: str
                 amount,   # type: Decimal
                 meta=None # type: dict
                 ):
        assert isinstance(method, str), "parameter should be str type"
        assert isinstance(amount, (Decimal, int)), "parameter should be Decimal type"
        if meta is not None:
            assert isinstance(meta, dict), "parameter should be dict type"
        self.method = method
        self.amount = amount
        self.meta = meta
    
    def jsonify(self):
        return self.__dict__
        
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Payment

        return cls(**json_dict)