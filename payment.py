from typing import List
from asset import Asset
from itertools import groupby
import cardanocli
import config
import data
from nft import Nft, nft_to_asset
from utxo import Utxo

#TODO return a payment result
def return_payment(payment_id: int, payment_addr: str, utxo: Utxo):
    print(f"Returning payment {payment_id} {utxo}")
    
    tx_draft_path = f"/tmp/txn_refund_{payment_id}.draft"
    tx_raw_path = f"/tmp/txn_refund_{payment_id}.raw"
    tx_signed_path = f"/tmp/txn_refund_{payment_id}.signed"

    all_utxo_assets = [utxo.lovelace] + utxo.other_assets
    min_return_lovelace = cardanocli.calculate_min_value(all_utxo_assets)
    cardanocli.build_txn(
        utxo,
        [(payment_addr, all_utxo_assets)],
        0,
        tx_draft_path,
        None)
    min_fee = cardanocli.calculate_min_fee(tx_draft_path, 1, 1, 1)
    print(f"RETURN min fee {min_fee} min value {min_return_lovelace}")

    # if we don't have enough lovelace to process the transaction, stop
    if utxo.lovelace.amount < min_fee + min_return_lovelace:
        data.insert_insufficient_funds_for_return(payment_id, min_return_lovelace, min_fee)
        raise Exception(f"Not enough lovelace ({utxo.lovelace.amount}) to cover fees & min value ({min_fee}, {min_return_lovelace})")

    new_lovelace_output = Asset("lovelace", utxo.lovelace.amount - min_fee)
    cardanocli.build_txn(
        utxo,
        [(payment_addr, [new_lovelace_output] + utxo.other_assets)],
        min_fee,
        tx_raw_path,
        None)

    receive_skey_path = config.config("payment_keys")["receive_skey_path"]
    cardanocli.sign_txn(tx_raw_path, tx_signed_path, [receive_skey_path])
    tx_id = cardanocli.submit_txn(tx_signed_path)
    print(f"Payment {payment_id} refunded w/ txn {tx_id}.")

    return tx_id

def send_pack(pack_id: int, payment_id: int, payment_addr: str, utxo: Utxo):
    print(f"Sending pack {pack_id} for payment {payment_id}")

    tx_draft_path = f"/tmp/txn_mint_{payment_id}.draft"
    tx_raw_path = f"/tmp/txn_mint_{payment_id}.raw"
    tx_signed_path = f"/tmp/txn_mint_{payment_id}.signed"
    tx_metadata_path = f"/tmp/txn_mint_{payment_id}.json"
    treasury_addr = config.config("address")["treasury_addr"]

    payment_keys = config.config("payment_keys")
    receive_skey_path = payment_keys["receive_skey_path"]
    minting_skey_path = payment_keys["minting_skey_path"]

    # get packs
    pack_nfts = data.get_pack_nfts(pack_id)
    if len(pack_nfts) == 0:
        raise Exception(f"Pack {pack_id} has no NFTs assigned to it")

    pack_assets = [nft_to_asset(n) for n in pack_nfts]
    min_send_lovelace = cardanocli.calculate_min_value(pack_assets)
    send_assets = [Asset("lovelace", min_send_lovelace)] + pack_assets
    treasury_lovelace = Asset("lovelace", utxo.lovelace.amount - min_send_lovelace)
    mint_def = { 'assets': pack_assets, 'metadata_path': tx_metadata_path }
    print(f"Assets to send {send_assets}") 

    # write metadata
    create_metadata_file(tx_metadata_path, pack_nfts)

    # calculate min fee
    cardanocli.build_txn(
        utxo,
        [
            (payment_addr, send_assets)
            , (treasury_addr, [treasury_lovelace] + utxo.other_assets)
        ],
        0,
        tx_draft_path,
        mint_def)
    min_fee = cardanocli.calculate_min_fee(tx_draft_path, 1, 2, 2)

    # setup transaction w/ proper fees
    treasury_lovelace = Asset("lovelace", utxo.lovelace.amount - min_send_lovelace - min_fee)
    cardanocli.build_txn(
        utxo,
        [
            (payment_addr, send_assets)
            , (treasury_addr, [treasury_lovelace] + utxo.other_assets)
        ],
        min_fee,
        tx_raw_path,
        mint_def)

    cardanocli.sign_txn(tx_raw_path, tx_signed_path, [receive_skey_path, minting_skey_path])
    tx_id = cardanocli.submit_txn(tx_signed_path)
    print(f"Payment {payment_id} sent pack {pack_id} w/ txn {tx_id}.")

    return tx_id

def create_metadata_file(path: str, nfts: List[Nft]):
    with open(path, 'w') as metadata_file:
        metadata_file.write(f"""{{
            \"721\": {{""")
        
        for policy_id, assets in groupby(nfts, lambda n: n.policy_id):
            metadata_file.write(f"\"{nfts[0].policy_id}\": {{")
            entries = []
            for asset_name, ns in groupby(assets, lambda n: n.asset_name):
                n = list(ns)[0]
                entries.append(f"\"{n.asset_name}\": {n.metadata_json}\n")
            metadata_file.write(",".join(entries))
            metadata_file.write(f"}}")

        metadata_file.write(f"}} }}")
