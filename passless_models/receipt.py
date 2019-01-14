from datetime import datetime
from decimal import Decimal
import json
import dateutil.parser
import jsonpickle

from .price import Price
from .item import Item
from .payment import Payment
from .vendor import Vendor
from .fee import Fee
from .loyalty import Loyalty

class Receipt():
    # TODO: add totalChange?
    # TODO: Add cashier?
    # TODO: Make totalDiscount and totalFee optional?
    # NOTE: 'global' discounts should be applied to individual items
    def __init__(self, 
                 time,                    # type: datetime 
                 currency,                # type: str
                 subTotal,                # type: Price
                 totalDiscount,           # type: Price
                 totalPrice,              # type: Price
                 totalFee,                # type: Price
                 totalPaid,               # type: Decimal
                 items,                   # type: List[Item]
                 payments,                # type: List[Payment]
                 vendor,                  # type: Vendor
                 vendorReference,         # type: str
                 fees=None,               # type: List[Fee]
                 loyalties=None,          # type: List[Loyalty]
                 ):
        # type: () -> None
        assert sum(map(lambda i: i['subTotal']['withoutTax'], items)) == subTotal['withoutTax'], "items subTotal does not add up to subTotal"
        # TODO: assert discounts add up
        # TODO: assert fees add up
        # TODO: assert payments add up
        # TODO: assert totalPrice adds up
        self.time = time
        self.currency = currency
        self.subTotal = subTotal
        self.totalDiscount = totalDiscount
        self.totalPrice = totalPrice
        self.totalFee = totalFee
        self.totalPaid = totalPaid
        self.items = items
        self.payments = payments
        self.vendor = vendor
        self.vendorReference = vendorReference
        self.fees = fees
        self.loyalties = loyalties

    def to_json(self):
        # type: () -> str
        return jsonpickle.encode(self, unpicklable=False)
        # return json.dumps(self, default=lambda o: o.__dict__, 
        #     sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, json_str):
        # type: (str) -> Receipt
        json_dict = json.loads(json_str)
        return cls.from_json_dict(json_dict)
    
    @classmethod
    def from_json_dict(cls, json_dict):
        result = cls(**json_dict)
        result.time = dateutil.parser.parse(json_dict['time'])
        result.subTotal = Price.from_json_dict(json_dict['subTotal'])
        result.totalDiscount = Price.from_json_dict(json_dict['totalDiscount'])
        result.totalPrice = Price.from_json_dict(json_dict['totalPrice'])
        result.totalFee = Price.from_json_dict(json_dict['totalFee'])
        result.items = list(map(Item.from_json_dict, json_dict['items']))
        result.payments = list(map(Payment.from_json_dict, json_dict['payments']))
        result.vendor = Vendor.from_json_dict(json_dict['vendor'])
        result.loyalties = list(map(Loyalty.from_json_dict, json_dict.get('loyalties', [])))
        result.fees = list(map(Fee.from_json_dict, json_dict.get('fees', [])))
        
        return result