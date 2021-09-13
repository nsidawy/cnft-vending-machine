from asset import Asset
import cardanocli
import config
import data
from utxo import Utxo

#TODO return a payment result
def return_payment(payment_id: int, payment_addr: str, utxo: Utxo):
    print(f"Returning payment {payment_id} {utxo}")
    
    tx_draft_path = f"/tmp/txn_{payment_id}.draft"
    tx_raw_path = f"/tmp/txn_{payment_id}.raw"
    tx_signed_path = f"/tmp/txn_{payment_id}.signed"

    receive_skey_path = config.config("payment_keys")["receive_skey_path"]
    all_utxo_assets = [utxo.lovelace] + utxo.other_assets

    min_return_lovelace = cardanocli.calculate_min_value(all_utxo_assets)
    cardanocli.build_txn(
        utxo,
        [(payment_addr, all_utxo_assets)],
        0,
        tx_draft_path)
    min_fee = cardanocli.calculate_min_fee(tx_draft_path, 1, 1, 1)
    print(f"RETURN min fee {min_fee} min value {min_return_lovelace}")

    # if we don't have enough lovelace to process the transaction, stop
    if utxo.lovelace.amount < min_fee + min_return_lovelace:
        raise Exception(f"Not enough lovelace ({utxo.lovelace.amount}) to cover fees & min value ({min_fee}, {min_return_lovelace})")

    new_lovelace_output = Asset("lovelace", utxo.lovelace.amount - min_fee)
    cardanocli.build_txn(
        utxo,
        [(payment_addr, [new_lovelace_output] + utxo.other_assets)],
        min_fee,
        tx_raw_path)

    cardanocli.sign_txn(tx_raw_path, tx_signed_path, [receive_skey_path])
    tx_id = cardanocli.submit_txn(tx_signed_path)
    print(f"Payment {payment_id} refunded w/ txn {tx_id}.")

def send_pack(pack_id: int, payment_id: int, payment_addr: str, utxo: Utxo):
    print(f"Sending pack {pack_id} for payment {payment_id}")
    pack_nfts = data.get_pack_nfts(pack_id)
    if len(pack_nfts) == 0:
        raise Exception(f"Pack {pack_id} has no NFTs assigned to it")

