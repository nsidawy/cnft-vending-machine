class PackType:                                                           
    def __init__(self, pack_type_id: str, description: str, lovelace_cost: int):
        self.pack_type_id = pack_type_id
        self.description = description
        self.lovelace_cost = lovelace_cost

    def __repr__(self):                                                
        return f'PackType {{ PackTypeId: {self.pack_type_id}, Description: {self.description}, LovelaceCost: {self.lovelace_cost} }}' 

