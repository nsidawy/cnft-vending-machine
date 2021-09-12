from typing import List
from asset import Asset

class Utxo:
    def __init__(self, tx_id: str, index_id: int, assets: List[Asset]):
        self.tx_id = tx_id
        self.index_id = index_id
        self.assets = assets

    def __str__(self):
        return f'Utxo {{ TxId: {self.tx_id}, Index: {self.index_id}, Assets: {self.assets} }}'

    def __repr__(self):
        return str(self)
