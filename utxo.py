from asset import Asset
from typing import List

class Utxo:                                                                               
    def __init__(self, txId: str, index: int, assets: List[Asset]):                       
        self.txId = txId                                                                  
        self.index = index                                                                
        self.assets = assets                                                              
                                                                                          
    def __str__(self):                                                                    
        return f'Utxo {{ TxId: {self.txId}, Index: {self.index}, Assets: {self.assets} }}'
                                                                                          
    def __repr__(self):                                                                   
        return f'Utxo {{ TxId: {self.txId}, Index: {self.index}, Assets: {self.assets} }}'
