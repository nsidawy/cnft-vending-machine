import os
import sys
import time
import traceback
import asset
import blockfrost
import cardanocli
import config
import data
import payment
from utxo import Utxo
import nft

def vend(config_path: str):
    config.set_config_file(config_path)
    set_environment()

    dipping_address = ''
    
    while True:
        try:
            utxos = cardanocli.get_utxos(v.address)
            for utxo in utxos:
                process_utxo(utxo, v, vending_to_packtypes_dict[v.id])
        except:
            print(traceback.format_exc())

        time.sleep(5)

def process_utxo(utxo: Utxo):
    try:
        #payment_addr = blockfrost.get_tx_payment_addr(utxo.tx_id)
        ## get payment ID
        #payment_id = data.get_payment_id(utxo.tx_id, utxo.index_id)
        #if payment_id is None:
        #    payment_id = data.insert_payment(
        #        utxo.tx_id
        #        , utxo.index_id
        #        , utxo.lovelace.amount
        #        , utxo.other_assets
        #        , payment_addr
        #        , vending_address.id)
        #    print(f"Inserted new payment {payment_id} for {utxo.tx_id}#{utxo.index_id}")
        #else:
        #    #TODO: Check if the payment is handled already. if so then continue to next tuxo
        #    return

        try:
            print("wip")
        except:
            #TODO: Log exception with payment
            print(traceback.format_exc())
            data.insert_error_log(payment_id, traceback.format_exc())
    except:
        # erroring here is unlikley but we don't want to block the utxo loop
        print(traceback.format_exc())

def is_valid_utxo(utxo: Utxo) -> bool:
    # require a minimum of 5 ada
    min_lovelace = 5000000
    if utxo.lovelace.amount < min_lovelace:
        print(f'Dipping payment does not have enough lovelace ({utxo.lovelace}, minimum: {min_lovelace}).') 
        return False

    # require exactly 2 dipping assets
    dipping_asset_count = 2
    if len(utxo.other_assets) != dipping_asset_count:
        print(f'Dipping payment does not contain exactly {dipping_asset_count} assets: {utxo.other_assets}')
        return False

    # check that both assets exist in our database
    assets = [nft.get_nft_from_asset(a) for a in utxo.other_assets]
    for i in range(len(assets)):
        if assets[i] is None:
            print(f'Asset {utxo.other_assets[i]} was not found in database')
            return False
    
    # confirm that there is exactly 1 of each asset
    # this shouldn't be possible unless our minting made a mistake...
    if any(a.amount != 1 for a in utxo.other_assets):
        print(f'There is more than 1 of at least one asset: {utxo.other_assets}')
        return False

    return True

def set_environment():
    environment = config.config("environment")
    for key in environment:
        os.environ[key.upper()] = environment[key]
