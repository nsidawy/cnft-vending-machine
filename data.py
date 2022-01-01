from typing import List, Optional
from cardanocli import Asset
from cardanocli import get_multi_asset_str
from nft import Nft
from packtype import PackType
import pquery

def throw_if_pack_missing(pack_id: int):
    has_row = pquery.read(f"""
        SELECT EXISTS (
            SELECT *
            FROM packs
            WHERE packid = {pack_id}
        )
    """)[0][0]
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
    """)[0][0]
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
    """)[0][0]
    if not has_row:
        raise Exception(f'Table packs does not have row for packId {pack_id} with a NULL mintingTxId')

    pquery.write(f"""
        UPDATE packs
        SET mintingTxId = '{minting_tx_id}'
        WHERE packId = {pack_id};
    """)

def insert_payment(tx_id: str, index_id: int, lovelace: int, other_assets: List[Asset], payment_address: str, vending_address_id: Optional[int]) -> int:
    vending_address_id_sql = "NULL" if vending_address_id is None else str(vending_address_id)
    pquery.write(f"""
        INSERT INTO payments (
            txId
            , indexId
            , lovelace
            , otherAssets
            , paymentAddress
            , vendingAddressId
        )
        SELECT '{tx_id}'
            , {index_id}
            , {lovelace}
            , '{get_multi_asset_str(other_assets)}'
            , '{payment_address}'
            , {vending_address_id_sql}
    """)

    return pquery.read(f"""
        SELECT paymentid
        FROM payments
        WHERE txId = '{tx_id}'
            AND indexId = {index_id}
    """)[0][0]

def get_payment_id(tx_id: str, index_id: int):
    results = pquery.read(f"""
        SELECT paymentid
        FROM payments
        WHERE txid = '{tx_id}'
            AND indexid = {index_id}
    """)

    if len(results) == 0:
        return None
    return results[0][0]

def insert_payment_refund(payment_id: int, refund_tx_id: str):
    results = pquery.write(f"""
        INSERT INTO refunds(paymentId, refundTxId)
        SELECT {payment_id}, '{refund_tx_id}'
    """)

def insert_insufficient_funds_for_return(payment_id: int, min_value: int, min_fee: int):
    results = pquery.write(f"""
        INSERT INTO insufficientFundsForReturn(paymentId, minValue, minFee)
        SELECT {payment_id}, {min_value}, {min_fee}
    """)

def insert_error_log(payment_id: int, error_message: str):
    escaped = error_message.replace("'", "''")
    results = pquery.write(f"""
        INSERT INTO errorLog(paymentId, errorMessage)
        SELECT {payment_id}, '{escaped}'
    """)

def get_pack_to_sell(pack_type_id) -> Optional[int]:
    results = pquery.read(f"""
        SELECT packId
        FROM packs
        WHERE packTypeId = {pack_type_id}
            AND paymentId IS NULL
        LIMIT 1
    """)

    if len(results) == 0:
        return None

    return results[0][0]

def get_pack_nfts(pack_id) -> List[Nft]:
    results = pquery.read(f"""
        SELECT n.nftId, n.policyId, n.assetName, metadatajson
        FROM nfts n
        JOIN packContents pc
            ON n.nftId = pc.nftId
        WHERE packId = {pack_id}
    """)

    return [Nft(result[0], result[1], result[2], result[3]) for result in results]
