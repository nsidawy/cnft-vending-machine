import pquery
from typing import List
from cardanocli import Asset
from cardanocli import get_multi_asset_str
from packtype import PackType

def throw_if_pack_missing(pack_id: int):
    has_row = pquery.read(f"""
        SELECT EXISTS (
            SELECT *
            FROM packs
            WHERE packid = {pack_id}
        )
    """)[0][0];
    if not has_row:
        raise Exception(f'Table packs does not have row for packId {pack_id}')

def update_pack_paymentid(pack_id: int, payment_id: int):
    throw_if_pack_missing(pack_id)

    has_row = pquery.read(f"""
        SELECT EXISTS (
            SELECT *
            FROM packs
            WHERE packid = {pack_id}
                AND paymentId IS NULL
        )
    """)[0][0];
    if not has_row:
        raise Exception(f'Table packs does not have row for packId {pack_id} with a NULL payment_id')

    pquery.write(f"""
        UPDATE packs
        SET paymentId = {payment_id}
        WHERE packId = {pack_id}
    """)

def update_pack_mintingtxid(pack_id: int, minting_tx_id: str):
    throw_if_pack_missing(pack_id)

    has_row = pquery.read(f"""
        SELECT EXISTS (
            SELECT *
            FROM packs
            WHERE packId = {pack_id}
                AND mintingTxId IS NULL
        )
    """)[0][0];
    if not has_row:
        raise Exception(f'Table packs does not have row for packId {pack_id} with a NULL mintingTxId')

    pquery.write(f"""
        UPDATE packs
        SET mintingTxId = '{minting_tx_id}'
        WHERE packId = {pack_id};
    """)

def insert_payment(tx_id: str, index_id: int, lovelace: int, other_assets: List[Asset], payment_address: str) -> int:
    pquery.write(f"""
        INSERT INTO payments (
            txId
            , indexId
            , lovelace
            , otherAssets
            , paymentAddress
        )
        SELECT '{tx_id}'
            , {index_id}
            , {lovelace}
            , '{get_multi_asset_str(other_assets)}'
            , '{payment_address}'
    """)

    return pquery.read(f"""
        SELECT paymentid
        FROM payments
        WHERE txId = '{tx_id}'
            AND indexId = {index_id}
    """)[0][0];

def get_payment_id(tx_id: str, index_id: int):
    results = pquery.read(f"""
        select paymentid
        from payments
        where txid = '{tx_id}'
            and indexid = {index_id}
    """)

    if len(results) == 0:
        return None
    return results[0][0]

def get_pack_dict():
    results = pquery.read(f"""
        SELECT packTypeId, description, lovelaceCost
        FROM packTypes
    """)

    if len(results) == 0:
        raise Exception("packtypes table is empty")

    return {packtype[2]: PackType(packtype[0], packtype[1], packtype[2]) for packtype in results}
