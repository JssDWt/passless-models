from .price import Price

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