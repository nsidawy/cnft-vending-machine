from typing import Optional
from app.utils import pquery
from app.data.vendingaddress import VendingAddress

class PackType:
    def __init__(self, pack_type_id: str, description: str, lovelace_cost: int, vending_address_id: Optional[int]):
        self.pack_type_id = pack_type_id
        self.description = description
        self.lovelace_cost = lovelace_cost
        self.vending_address_id = vending_address_id

    def __str__(self):
        return f'packtype {{ packtypeid: {self.pack_type_id}, description: {self.description}, lovelacecost: {self.lovelace_cost}, vendingaddressid: {self.vending_address_id} }}'

    def __repr__(self):
        return f'packtype {{ packtypeid: {self.pack_type_id}, description: {self.description}, lovelacecost: {self.lovelace_cost}, vendingaddressid: {self.vending_address_id} }}'

def get_packtypes_dict(vending_address: VendingAddress):
    where_clause = "" if vending_address.id is None else f"WHERE vendingAddressId = {vending_address.id}"
    results = pquery.read(f"""
        SELECT packTypeId, description, lovelaceCost, vendingAddressId
        FROM packTypes
        {where_clause}
    """)

#    if len(results) == 0:
#        raise Exception("packtypes table is empty")

    return {packtype[2]: PackType(packtype[0], packtype[1], packtype[2], packtype[3]) for packtype in results}
