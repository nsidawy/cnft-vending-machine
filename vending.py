import time
import sys
import traceback
from datetime import datetime
import asset
import blockfrost
import cardanocli
import config
import data

def vend():
    addresses = config.config("address")
    treasury_addr = addresses["treasury_addr"]
    receive_addr = addresses["receive_addr"]
    receive_skey_path = addresses["receive_skey_path"]
    minting_skey_path = addresses["minting_skey_path"]
    lovelace_to_packtypes = data.get_pack_dict()

    print(lovelace_to_packtypes)

    while True:
        try:
            utxos = cardanocli.get_utxos(receive_addr)
            for utxo in utxos:
                payment_addr = blockfrost.get_tx_payment_addr(utxo.tx_id)
                (lovelace_asset, other_assets) = asset.get_lovelace_and_other_assets(utxo.assets)

                # get payment ID
                payment_id = data.get_payment_id(utxo.tx_id, utxo.index_id)
                if payment_id is None:
                    payment_id = data.insert_payment(
                        utxo.tx_id
                        , utxo.index_id
                        , lovelace_asset.amount
                        , other_assets
                        , payment_addr)



        except Exception:
            print(traceback.format_exc())

        time.sleep(5)

def update_print():
    old_f = sys.stdout
    class DebugWriter:
        def write(self, x):
            now = datetime.now().strftime("%H:%M:%S")
            old_f.write(x.replace("\n", " [%s]\n" % now))
    sys.stdout = DebugWriter()
