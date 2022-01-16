import copy
import json
import os
import sys
import time
import traceback
from typing import Optional, Tuple
from app.utils import blockfrost, cardanocli, config, payment, pinata
from app.data import asset, dip, queries, nft
from app.data.utxo import Utxo
import app.the_dipper.main as dipper

def vend(config_path: str):
    config.set_config_file(config_path)
    set_environment()

    dipping_address = config.config('address')['dipping_addr']
    
    while True:
        try:
            utxos = cardanocli.get_utxos(dipping_address)
            for utxo in utxos:
                process_utxo(utxo)
        except:
            print(traceback.format_exc())

        time.sleep(5)

def process_utxo(utxo: Utxo):
    dipping_skey_path = config.config('payment_keys')['dipping_skey_path']
    try:
        payment_addr = blockfrost.get_tx_payment_addr(utxo.tx_id)
        # get payment ID
        payment_id = queries.get_payment_id(utxo.tx_id, utxo.index_id)
        if payment_id is None:
            payment_id = queries.insert_payment(
                utxo.tx_id
                , utxo.index_id
                , utxo.lovelace.amount
                , utxo.other_assets
                , payment_addr
                , None)
            print(f"Inserted new payment {payment_id} for {utxo.tx_id}#{utxo.index_id}")
        else:
            #TODO: Check if the payment is handled already. if so then continue to next tuxo
            return

        try:
            # require a minimum of 5 ada
            min_lovelace = 5000000
            if utxo.lovelace.amount < min_lovelace:
                print(f'Dipping payment does not have enough lovelace ({utxo.lovelace}, minimum: {min_lovelace}).') 
                payment.return_payment(payment_id, payment_addr, dipping_skey_path, utxo)
                return 

            dipping_inputs = get_dipping_inputs(utxo)
            if dipping_inputs is None:
                payment.return_payment(payment_id, payment_addr, dipping_skey_path, utxo)
                return
            (nugget_nft, sauce_nft, dipping_index) = dipping_inputs

            # execute the dip
            dipped_nft = execute_dip(nugget_nft, sauce_nft, dipping_index)
            payment.send_dip(payment_id, payment_addr, dipping_skey_path, utxo, nugget_nft, sauce_nft, dipped_nft)
            dip.insert(payment_id, nugget_nft.nft_id, sauce_nft.nft_id, dipped_nft.nft_id)
        except:
            print(traceback.format_exc())
            queries.insert_error_log(payment_id, traceback.format_exc())
    except:
        # erroring here is unlikley but we don't want to block the utxo loop
        print(traceback.format_exc())

def execute_dip(nugget: nft.Nft, sauce: nft.Nft, dipping_index: int) -> nft.Nft:
    nugget_metadata = json.loads(nugget.metadata_json)
    sauce_metadata = json.loads(sauce.metadata_json)

    # get dip parameters
    nugget_id = int(nugget_metadata['attributes']['Id'])
    dipping_config = config.config("dipping")
    nugget_base_path = dipping_config['nugget_base_path']
    output_path = dipping_config['output_path']

    # pull sauce types
    if dipping_index == 0:
        sauce_type_1 = sauce_metadata['attributes']['Type']
        sauce_type_2 = None
    # dipping index == 1
    else:
        sauce_type_1 = nugget_metadata['attributes']['Sauce 1']
        sauce_type_2 = sauce_metadata['attributes']['Type']

    (png_path, mp4_path, dipped_sauce_type_1, dipped_sauce_type_2) = dipper.dip(
            nugget_base_path, nugget_id, sauce_type_1, sauce_type_2, output_path)

    # upload assets to IPFS
    print(f'Uploading {png_path} to IPFS')
    png_ipfs_hash = pinata.upload_file(png_path)
    print(f'Uploading {mp4_path} to IPFS')
    mp4_ipfs_hash = pinata.upload_file(mp4_path)

    # delete local assets
    os.remove(png_path)
    os.remove(mp4_path)

    # construct dipped metadata
    dipped_metadata = copy.deepcopy(nugget_metadata)
    dipped_metadata['image'] = f'ipfs://{png_ipfs_hash}'
    dipped_metadata['files'] = [{
        'src': f'ipfs://{mp4_ipfs_hash}',
        'name': 'Nugget',
        'mediaType': 'video/mp4'
        }]
    dipped_metadata['attributes']['Sauce 1'] = dipped_sauce_type_1
    dipped_metadata['attributes']['Sauce 2'] = dipped_sauce_type_2 if dipped_sauce_type_2 is not None else 'None'

    return nft.insert(nugget.policy_id, nugget.asset_name + 'D', json.dumps(dipped_metadata))

def get_dipping_inputs(utxo: Utxo) -> Optional[Tuple[nft.Nft, nft.Nft, int]]:
    # get dipping information from utxo
    dipping_nfts = get_nugget_and_sauce(utxo)
    if dipping_nfts is None:
        print(f'Utxo does not have valid nugget and sauce NFT')
        return None
    (nugget, sauce) = dipping_nfts
    dipping_index = get_dipping_index(nugget)
    if dipping_index is None:
        print('Nugget has already been double-dipped.')
        return None

    return (nugget, sauce, dipping_index)

def get_nugget_and_sauce(utxo: Utxo) -> Optional[Tuple[nft.Nft, nft.Nft]]:
    # require exactly 2 dipping assets
    expected_asset_count = 2
    if len(utxo.other_assets) != expected_asset_count:
        print(f'Dipping payment does not contain exactly {expected_asset_count} assets: {utxo.other_assets}')
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
