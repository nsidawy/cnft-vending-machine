from typing import List, Tuple
import config
import pquery
from asset import Asset

class Treasury:
    def __init__(self, address: str, share_percent: float):
        self.address = address
        self.share_percent = share_percent

    def __str__(self):
        return f'{self.share_percent} {self.address}'

    def __repr__(self):
        return f'Treasury {{ Address: {self.address}, SharePercent: {self.share_percent} }}'

def get_treasuries() -> List[Treasury]:
    config_addresses = config.config("address")
    # If defined in a config file, then just use that as the sole treasury address.
    # Done for backwards compatibility
    if "treasury_addr" in config_addresses:
        return [Treasury(config_addresses["treasury_addr"], 1)]

    results = pquery.read("""
        SELECT address, sharePercent
        FROM treasuries
    """)

    treasuries = [Treasury(r[0], r[1]) for r in results]
    if sum([t.share_percent for t in treasuries]) != 1.0:
        raise Exception(f"Sum of treasury shares does not equal 100% (1.0)\n{treasuries}")
    return treasuries

# Splits up lovelace amount across treasury addresses by share perecent.
def get_outputs(treasuries: List[Treasury], lovelace: int) -> List[Tuple[str, List[Asset]]]:
    outputs = [(t.address, Asset("lovelace", int(t.share_percent * lovelace))) for t in treasuries]

    remainder = lovelace - sum([o[1].amount for o in outputs])
    if remainder > 0:
        outputs[0] = (outputs[0][0], Asset("lovelace", outputs[0][1].amount + remainder))

    return outputs
