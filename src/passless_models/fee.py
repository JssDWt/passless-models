from .price import Price
from .tax_class import TaxClass

class Fee():
    def __init__(self,
                 name,    # type: str
                 price,   # type: Price
                 taxClass # type: TaxClass
                 ):
        assert price.tax == price.withoutTax * taxClass.fraction, "Tax price not equal to tax rate"
        self.name = name
        self.price = price
        self.taxClass = taxClass
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Fee

        result = cls(**json_dict)
        result.price = Price.from_json_dict(json_dict['price'])
        result.taxClass = TaxClass.from_json_dict(json_dict['taxClass'])
        return result