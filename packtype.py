class PackType:
    def __init__(self, pack_type_id: str, description: str, lovelace_cost: int):
        self.pack_type_id = pack_type_id
        self.description = description
        self.lovelace_cost = lovelace_cost

    def __str__(self):
        return f'packtype {{ packtypeid: {self.pack_type_id}, description: {self.description}, lovelacecost: {self.lovelace_cost} }}'

    def __repr__(self):
        return f'packtype {{ packtypeid: {self.pack_type_id}, description: {self.description}, lovelacecost: {self.lovelace_cost} }}'

