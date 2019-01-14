from datetime import datetime
from decimal import Decimal
import json
import dateutil.parser
import jsonpickle

# TODO: Make tax a class in order to include percentage
# TODO: Add warranty and return time information
# TODO: Add shipping information if web is involved
# TODO: Add customer information
# TODO: Make sure the objects can be extended with extra props...don't break
# TODO: Account for rounding in price/tax assertions

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

class Price():
    def __init__(self,
                 withoutTax, # type: Double
                 withTax,    # type: Double
                 tax         # type: Double
                 ):
        assert withoutTax + tax == withTax, "tax does not add up."
        self.withoutTax = withoutTax
        self.withTax = withTax
        self.tax = tax
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Price

        return cls(**json_dict) 

class Discount():
    # TODO: Add description
    def __init__(self,
                 name,     # type: str
                 deduct    # type: Price
                 ):
        self.name = name
        self.deduct = deduct
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Discount

        result = cls(**json_dict) 
        result.deduct = Price.from_json_dict(json_dict['deduct'])
        return result

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

class Vendor():
    # TODO: Include difference between company and shop
    # TODO: Validate logo, find a decent logo format
    # TODO: Change kvkNumber to 'company registry'
    def __init__(self,
                 name,      # type: str
                 address,   # type: str
                 phone,     # type: str
                 vatNumber, # type: str
                 kvkNumber, # type: str
                 logo=None, # type: str
                 email=None,# type: str
                 web=None,  # type: str
                 meta=None, # type: dict
                 ):
        self.name = name
        self.address = address
        self.phone = phone
        self.vatNumber = vatNumber
        self.kvkNumber = kvkNumber
        self.logo = logo
        self.email = email
        self.web = web
        self.meta = meta
    
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Vendor

        return cls(**json_dict)

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
