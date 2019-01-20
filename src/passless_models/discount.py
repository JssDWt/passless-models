from .price import Price

class Discount():
    # TODO: Add description
    def __init__(self,
                 name,     # type: str
                 deduct    # type: Price
                 ):
        assert isinstance(name, str), "parameter should be str type"
        assert isinstance(deduct, Price), "parameter should be Price type"
        self.name = name
        self.deduct = deduct
    
    def jsonify(self):
        return self.__dict__
        
    @classmethod
    def from_json_dict(cls, json_dict):
        # type: (dict) -> Discount

        return cls(
            name=json_dict['name'],
            deduct=Price.from_json_dict(json_dict['deduct'])
        )