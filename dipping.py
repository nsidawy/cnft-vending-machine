import json
import os
import sys
import time
import traceback
from typing import Optional, Tuple
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
            utxos = cardanocli.get_utxos(dipping_address)
            for utxo in utxos:
                process_utxo(utxo)
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
        # require a minimum of 5 ada
        min_lovelace = 5000000
        if utxo.lovelace.amount < min_lovelace:
            print(f'Dipping payment does not have enough lovelace ({utxo.lovelace}, minimum: {min_lovelace}).') 
            #TODO return payment
            return 

        dipping_nfts = get_nugget_and_sauce(utxo)
        if dipping_nfts is None:
            print(f'Utxo does not have valid nugget and sauce NFT')
            #TODO return payment
            return 
        (nugget, sauce) = dupping_nfts
        dipping_index = get_dipping_index(nugget)
        if dipping_index is None:
            print('Nugget has been double-dipped.')
            #TODO return payment
            return 

        try:
            print("wip")
        except:
            #TODO: Log exception with payment
            print(traceback.format_exc())
            #data.insert_error_log(payment_id, traceback.format_exc())
    except:
        # erroring here is unlikley but we don't want to block the utxo loop
        print(traceback.format_exc())

def get_nugget_and_sauce(utxo: Utxo) -> Optional[Tuple[nft.Nft, nft.Nft]]:
    # require exactly 2 dipping assets
    dipping_asset_count = 2
    if len(utxo.other_assets) != dipping_asset_count:
        print(f'Dipping payment does not contain exactly {dipping_asset_count} assets: {utxo.other_assets}')
        return None

    # check that both assets exist in our database
    nft_0 = nft.get_nft_from_asset(utxo.other_assets[0])
    nft_1 = nft.get_nft_from_asset(utxo.other_assets[1])
    if nft_0 is None:
        print(f'Asset {utxo.other_assets[0]} was not found in database')
        return None
    if nft_1 is None:
        print(f'Asset {utxo.other_assets[1]} was not found in database')
        return None
    nfts = [nft_0, nft_1]
    
    # confirm that there is exactly 1 of each asset
    # this shouldn't be possible unless our minting made a mistake...
    if any(a.amount != 1 for a in utxo.other_assets):
        print(f'There is more than 1 of at least one asset: {utxo.other_assets}')
        return None

    nugget_nft = next((n for n in nfts if n.asset_name.startswith("Nugget")), None)
    sauce_nft = next((n for n in nfts if n.asset_name.startswith("Sauce")), None)
    if nugget_nft is None or sauce_nft is None:
        print(f'Expected 1 sauce and 1 nugget but got {nfts}')
        return None

    return (nugget_nft, sauce_nft)

def get_dipping_index(nugget: nft.Nft) -> Optional[int]:
    metadata = json.loads(nugget.metadata_json)

    if metadata['attributes']['Sauce 1'] == 'None':
        return 0
    elif metadata['attributes']['Sauce 2'] == 'None':
        return 1
    return None

def set_environment():
    environment = config.config("environment")
    for key in environment:
        os.environ[key.upper()] = environment[key]
