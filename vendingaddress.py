from typing import List, Optional
import config
import pquery

class VendingAddress:
    def __init__(self, id: Optional[int], address: str, signing_key_path: str):
        self.id = id
        self.address = address
        self.signing_key_path = signing_key_path

    def __str__(self):
        return f'VendingAddress {{ id: {self.id}, address: {self.address}, signingkeypath: {self.signing_key_path} }}'

    def __repr__(self):
        return f'VendingAddress {{ id: {self.id}, address: {self.address}, signingkeypath: {self.signing_key_path} }}'

def get_vending_addresses() -> List[VendingAddress]:
    config_addresses = config.config("address")
    # If defined in a config file, then just use that as the sole vending address.
    # Done for backwards compatibility
    if "receive_addr" in config_addresses:
        payment_key = config.config("payment_keys")["receive_skey_path"]
        return [VendingAddress(None, config_addresses["receive_addr"], payment_key)]

    results = pquery.read("""
        SELECT vendingAddressId, address, signingKeyPath
        FROM vendingAddresses
    """)

    if len(results) == 0:
        raise Exception("vendingAddresses table is empty")

    return [VendingAddress(r[0], r[1], r[2]) for r in results]
