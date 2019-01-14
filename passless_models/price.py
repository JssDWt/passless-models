from decimal import Decimal

class Price():
    def __init__(self,
                 withoutTax, # type: Decimal
                 withTax,    # type: Decimal
                 tax         # type: Decimal
                 ):
        assert withoutTax + tax == withTax, "tax does not add up."
        self.withoutTax = withoutTax
        self.withTax = withTax
        self.tax = tax
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Price

        return cls(**json_dict) 