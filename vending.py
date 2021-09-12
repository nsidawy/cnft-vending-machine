import time
import sys
import traceback
from datetime import datetime
import asset
import blockfrost
import cardanocli
import config
import data
import payment

def vend():
    addresses = config.config("address")
    receive_addr = addresses["receive_addr"]
    lovelace_to_packtypes = data.get_pack_types_dict()

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
                    print(f"Inserted new payment {payment_id} for {utxo.tx_id}#{utxo.index_id}")
                else: 
                    #TODO: Check if the payment is handled already. if so then continue to next tuxo

                bought_pack = lovelace_to_packtypes.get(lovelace_asset.amount)

                # handle incorrect payment amount
                if bought_pack is None:
                    print(f"Payment {payment_id} did not submit a valid payment amount: {lovelace_asset.amount}")
                    payment.return_payment(payment_id, payment_addr, utxo)
                    continue

                pack_id = data.get_pack_to_sell(bought_pack.pack_type_id)
                if pack_id is None:
                    print(f"No more packs remaining: {bought_pack}")
                    payment.return_payment(payment_id, payment_addr, utxo)
                    continue

                payment.send_pack(pack_id, payment_id, payment_addr, utxo)

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
