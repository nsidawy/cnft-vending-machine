from asset import Asset
from typing import List

class Utxo:                                                                               
    def __init__(self, tx_id: str, index_id: int, assets: List[Asset]):                       
        self.tx_id = tx_id                                                                  
        self.index_id = index_id
        self.assets = assets                                                              
                                                                                          
    def __str__(self):                                                                    
        return f'Utxo {{ TxId: {self.txId}, Index: {self.index}, Assets: {self.assets} }}'
                                                                                          
    def __repr__(self):                                                                   
        return f'Utxo {{ TxId: {self.txId}, Index: {self.index}, Assets: {self.assets} }}'
