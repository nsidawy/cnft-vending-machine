from typing import List
from app.data.asset import Asset, get_lovelace_and_other_assets

class Utxo:
    def __init__(self, tx_id: str, index_id: int, assets: List[Asset]):
        self.tx_id = tx_id
        self.index_id = index_id
        (lovelace, other_assets) = get_lovelace_and_other_assets(assets)
        self.lovelace = lovelace
        self.other_assets = other_assets

    def __str__(self):
        return f'Utxo {{ TxId: {self.tx_id}, Index: {self.index_id}, Lovelace: {self.lovelace}, OtherAssets: {self.other_assets} }}'

    def __repr__(self):
        return str(self)
