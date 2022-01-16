import json
import requests
from app.utils import config

def get_tx_payment_addr(tx_id: str):
    blockfrost_config = config.config("blockfrost")

    response = requests.get(f'{blockfrost_config["base_address"]}/txs/{tx_id}/utxos'
            , headers = { "project_id": blockfrost_config["project_id"] })
    if response.status_code != 200:
        raise Exception(f'Error reaching BlockFrost API to get txn information for tx ID {tx_id}\n{response.text}')

    response_json = json.loads(response.text)

    # Return the first input address found since transactions might have multiple
    # payment utxos from different addresses. This is common if someone is sending
    # payment from a wallet (e.g. Daedalus) since it will automatically construct a
    # transaction from combinations of utxos in the wallet.
    return response_json["inputs"][0]["address"]
