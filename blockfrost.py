import config
import requests
import json

def get_tx_input_address(txId: str):
    blockfrostConfig = config.config("blockfrost") 

    r = requests.get(f'{blockfrostConfig["base_address"]}/txs/{txId}/utxos'
            , headers = { "project_id": blockfrostConfig["project_id"] })
    if r.status_code != 200:
        raise Exception(f'Error reaching BlockFrost API to get txn information for tx ID {txId}\n{r.text}')

    response_json = json.loads(r.text)
    return response_json["inputs"][0]["address"]
