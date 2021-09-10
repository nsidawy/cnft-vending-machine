import pquery

def throw_if_pack_missing(pack_id: int):
    has_row = pquery.read(f"""
        SELECT count(*)
        FROM packs
        WHERE packid = {pack_id};
    """);
    if has_row[0][0] == 0:
        raise Exception(f'Table packs does not have row for packId {pack_id}')

def update_pack_paymenttxid(pack_id: int, payment_tx_id: str):
    throw_if_pack_missing(pack_id)

    has_row = pquery.read(f"""
        SELECT count(*)
        FROM packs
        WHERE packid = {pack_id}
            AND paymentTxId IS NULL
    """);
    if has_row[0][0] == 0:
        raise Exception(f'Table packs does not have row for packId {pack_id} with a NULL paymentTxId')

    pquery.write(f"""
        UPDATE packs
        SET paymentTxId = '{payment_tx_id}'
        WHERE packId = {pack_id};
    """)

def update_pack_mintingtxid(pack_id: int, minting_tx_id: str):
    throw_if_pack_missing(pack_id)

    has_row = pquery.read(f"""
        SELECT count(*)
        FROM packs
        WHERE packid = {pack_id}
            AND mintingTxId IS NULL
    """);
    if has_row[0][0] == 0:
        raise Exception(f'Table packs does not have row for packId {pack_id} with a NULL mintingTxId')

    pquery.write(f"""
        UPDATE packs
        SET mintingTxId = '{minting_tx_id}'
        WHERE packId = {pack_id};
    """)
