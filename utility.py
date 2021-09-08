import subprocess

class Asset:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __str__(self):
        return f'Asset {{ Name: {self.name}, Amount: {self.amount} }}'

    def __repr__(self):
        return str(self)

class Utxo:
    def __init__(self, txId: str, index: int, assets: [Asset]):
        self.txId = txId
        self.index = index
        self.assets = assets

    def __str__(self):
        return f'Utxo {{ TxId: {self.txId}, Index: {self.index}, Assets: {self.assets} }}'

    def __repr__(self):
        return str(self)

def getUtxos(address) -> [Utxo]:
    process = subprocess.run(["cardano-cli", "query", "utxo", "--mainnet", "--address", address], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting UTXOs for address {address}\n{process.stderr.decode("UTF-8")}')

    lines = process.stdout.decode("UTF-8").split("\n")
    utxoLines = lines[2:]
    utxos = []

    for utxoLine in utxoLines:
        if utxoLine == "":
            continue
        utxoLineSplit = list(filter(None, utxoLine.split(" ")))

        assetStrs = list(filter(lambda s: s != "+", utxoLineSplit[2:]))
        assets = []
        for i in range(int(len(assetStrs)/2)):
            assets.append(Asset(assetStrs[i*2+1], int(assetStrs[i*2])))

        utxos.append(Utxo(utxoLineSplit[0], int(utxoLineSplit[1]), assets))

    return utxos
