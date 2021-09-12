import subprocess
import config
from typing import List
from utxo import Utxo
from asset import *

def get_protocol_params_path():
    return config.config("params_file")["path"]

def get_utxos(address) -> List[Utxo]:
    process = subprocess.run([
            "cardano-cli", "query", "utxo"
            , "--mainnet"
            , "--address", address]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting UTXOs for address {address}\n{process.stderr.decode("UTF-8")}')

    lines = process.stdout.decode("UTF-8").split("\n")
    utxoLines = lines[2:]
    utxos = []

    for utxoLine in utxoLines:
        if utxoLine == "":
            continue
        utxoLineSplit = list(filter(None, utxoLine.split(" ")))

        multi_asset_str = " ".join(utxoLineSplit[2:])
        assets = get_assets_from_str(multi_asset_str)

        utxos.append(Utxo(utxoLineSplit[0], int(utxoLineSplit[1]), assets))

    return utxos

def get_tx_id(signed_tx_path) -> str:
    process = subprocess.run([
            "cardano-cli", "transaction", "txid"
            , "--tx-file", signed_tx_path]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting tx ID for signed tx file {signed_tx_path}\n{process.stderr.decode("UTF-8")}')

    return process.stdout.decode("UTF-8").strip()

def calculate_min_value(assets: List[Asset]) -> int:
    multi_asset = get_multi_asset_str(assets)

    process = subprocess.run([
            "cardano-cli", "transaction", "calculate-min-value"
            , "--protocol-params-file", get_protocol_params_path()
            , "--multi-asset", multi_asset]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error calculating min value for assets {assets}\n{process.stderr.decode("UTF-8")}')

    out = process.stdout.decode("UTF-8").strip()
    min_value = int(out.split(" ")[1])
    return min_value

def calculate_min_fee(tx_body_file: str, tx_in_count: int, tx_out_count: int, witness_count: int) -> int:

    process = subprocess.run([
            "cardano-cli", "transaction", "calculate-min-fee"
            , "--protocol-params-file", get_protocol_params_path()
            , "--mainnet"
            , "--tx-body-file", tx_body_file
            , "--tx-in-count", str(tx_in_count)
            , "--tx-out-count", str(tx_out_count)
            , "--witness-count", str(witness_count)]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error calculating min fee for txn {tx_body_file}\n{process.stderr.decode("UTF-8")}')

    out = process.stdout.decode("UTF-8").strip()
    fee = int(out.split(" ")[0])
    return fee
