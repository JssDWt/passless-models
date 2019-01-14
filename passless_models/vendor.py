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