from decimal import Decimal

class TaxClass():
    def __init__(self,
                 name,     # type: str
                 fraction, # type: Decimal
                 ):
        assert fraction <= 1 and fraction >= 0, "fraction should be between 0 and 1"
        self.name = name
        self.fraction = fraction
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> TaxClass

        return cls(**json_dict) 