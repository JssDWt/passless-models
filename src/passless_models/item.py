from decimal import Decimal
from .price import Price
from .tax_class import TaxClass
from .discount import Discount

class Item():
    # TODO: Change name to Orderline
    # TODO: Add images?
    def __init__(self,
                 name,                    # type: str
                 quantity,                # type: Decimal
                 unit,                    # type: str
                 unitPrice,               # type: Price
                 subTotal,                # type: Price
                 totalDiscount,           # type: Price
                 totalPrice,              # type: Price
                 taxClass,                # type: TaxClass
                 shortDescription=None,   # type: str
                 description=None,        # type: str
                 brand=None,              # type: str
                 discounts=None,          # type: List[Discount]
                 ):
        assert subTotal['withTax'] - totalDiscount['withTax'] == totalPrice['withTax'], "subTotal - discount != total"
        assert subTotal['withoutTax'] - totalDiscount['withoutTax'] == totalPrice['withoutTax'], "subTotal - discount != total"
        assert unitPrice['withoutTax'] * quantity == subTotal['withoutTax'], "unitPrice * quantity != subTotal"
        assert unitPrice['withTax'] * quantity == subTotal['withTax'], "unitPrice * quantity != subTotal"
        assert unitPrice['tax'] == unitPrice['withoutTax'] * taxClass['fraction'], "Tax price not equal to tax rate"

        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.unitPrice = unitPrice
        self.subTotal = subTotal
        self.totalDiscount = totalDiscount
        self.totalPrice = totalPrice
        self.taxClass = taxClass
        self.shortDescription = shortDescription
        self.description = description
        self.brand = brand
        self.discounts = discounts
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Item

        result = cls(**json_dict)
        result.unitPrice = Price.from_json_dict(json_dict['unitPrice'])
        result.subTotal = Price.from_json_dict(json_dict['subTotal'])
        result.totalDiscount = Price.from_json_dict(json_dict['totalDiscount'])
        result.totalPrice = Price.from_json_dict(json_dict['totalPrice'])
        result.taxClass = TaxClass.from_json_dict(json_dict['taxClass'])
        result.discounts = list(map(Discount.from_json_dict, json_dict.get('discounts', [])))
        return result