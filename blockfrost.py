import config
import requests
import json

def get_tx_payment_addr(txId: str):
    blockfrostConfig = config.config("blockfrost") 

    r = requests.get(f'{blockfrostConfig["base_address"]}/txs/{txId}/utxos'
            , headers = { "project_id": blockfrostConfig["project_id"] })
    if r.status_code != 200:
        raise Exception(f'Error reaching BlockFrost API to get txn information for tx ID {txId}\n{r.text}')

    response_json = json.loads(r.text)

    # Return the first input address found since transactions might have multiple
    # payment utxos from different addresses. This is common if someone is sending
    # payment from a wallet (e.g. Daedalus) since it will automatically construct a 
    # transaction from combinations of utxos in the wallet.
    return response_json["inputs"][0]["address"]
