import json
from packaging import version
import subprocess
from typing import List, Tuple
from utxo import Utxo
from asset import Asset, get_assets_from_str, get_multi_asset_str
import config

def get_net_cli_arg():
    net_params = config.config("net")
    if net_params["is_testnet"] == "true":
        return ["--testnet-magic", net_params["testnet_magic"]]
    else:
        return ["--mainnet"]

def get_protocol_params_path() -> str:
    return config.config("params_file")["path"]

def get_cli_version() -> version.Version:
    process = subprocess.run(["cardano-cli", "version"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting CLI version.\n{process.stderr.decode("UTF-8")}')

    return version.Version(process.stdout.decode("UTF-8").split(" ")[1])

def get_utxos(address) -> List[Utxo]:
    process = subprocess.run([
            "cardano-cli", "query", "utxo"
            , "--address", address]
            + get_net_cli_arg()
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting UTXOs for address {address}\n{process.stderr.decode("UTF-8")}')

    lines = process.stdout.decode("UTF-8").split("\n")
    utxo_lines = lines[2:]
    utxos = []

    for utxo_line in utxo_lines:
        if utxo_line == "":
            continue
        utxo_line_split = list(filter(None, utxo_line.split(" ")))

        multi_asset_str = " ".join(utxo_line_split[2:])
        assets = get_assets_from_str(multi_asset_str)

        utxos.append(Utxo(utxo_line_split[0], int(utxo_line_split[1]), assets))

    return utxos

def get_tip_slot() -> int:
    process = subprocess.run([
            "cardano-cli", "query", "tip"]
            + get_net_cli_arg()
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting cardano tip\n{process.stderr.decode("UTF-8")}')

    return json.loads(process.stdout.decode("UTF-8").strip())["slot"]

def get_tx_id(signed_tx_path) -> str:
    process = subprocess.run([
            "cardano-cli", "transaction", "txid"
            , "--tx-file", signed_tx_path]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting tx ID for signed tx file {signed_tx_path}\n{process.stderr.decode("UTF-8")}')

    return process.stdout.decode("UTF-8").strip()

def calculate_min_value(address: str, assets: List[Asset]) -> int:
    multi_asset = get_multi_asset_str(assets)

    process = subprocess.run([
            "cardano-cli", "transaction", "calculate-min-required-utxo"
            , "--protocol-params-file", get_protocol_params_path()
            , "--tx-out", f'{address} {multi_asset}']
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
            , "--tx-body-file", tx_body_file
            , "--tx-in-count", str(tx_in_count)
            , "--tx-out-count", str(tx_out_count)
            , "--witness-count", str(witness_count)]
            + get_net_cli_arg()
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error calculating min fee for txn {tx_body_file}\n{process.stderr.decode("UTF-8")}')

    out = process.stdout.decode("UTF-8").strip()
    fee = int(out.split(" ")[0])
    return fee

def build_txn(
        utxo: Utxo
        , outputs: List[Tuple[str, List[Asset]]]
        , fee: int
        , tx_draft_path: str
        , mint_def
    ):
    tx_out_tuples = [["--tx-out", f"{output[0]}+{get_multi_asset_str(output[1])}"] for output in outputs]
    tx_outs = [item for sublist in tx_out_tuples for item in sublist]
    mint_args = []
    if mint_def is not None:
        mint_args.append("--mint")
        mint_args.append(get_multi_asset_str(mint_def["assets"]))
        mint_args.append("--metadata-json-file")
        mint_args.append(mint_def["metadata_path"])
        mint_args.append("--mint-script-file")
        mint_args.append(mint_def["mint-script-file"])

    process = subprocess.run([
            "cardano-cli", "transaction", "build-raw"
            , "--tx-in", f"{utxo.tx_id}#{utxo.index_id}"
            , "--fee", str(fee)
            , "--invalid-hereafter", str(get_tip_slot() + 1000)
            , "--out-file", tx_draft_path]
            + tx_outs
            + mint_args
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error building transaction\n{process.stderr.decode("UTF-8")}')

    return tx_draft_path

def sign_txn(tx_draft_path: str, tx_signed_path: str, key_paths: List[str]):
    signing_tuples = [["--signing-key-file", key_path] for key_path in key_paths]
    signings = [item for sublist in signing_tuples for item in sublist]
    process = subprocess.run([
            "cardano-cli", "transaction", "sign"
            , "--tx-body-file", tx_draft_path
            , "--out-file", tx_signed_path]
            + signings
            + get_net_cli_arg()
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error signing transaction\n{process.stderr.decode("UTF-8")}')

def submit_txn(tx_signed_path: str) -> str:
    process = subprocess.run([
            "cardano-cli", "transaction", "submit"
            , "--tx-file", tx_signed_path]
            + get_net_cli_arg()
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error signing transaction\n{process.stderr.decode("UTF-8")}')

    process = subprocess.run([
            "cardano-cli", "transaction", "txid"
            , "--tx-file", tx_signed_path]
        , stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    if process.returncode != 0:
        raise Exception(f'Error getting tx ID\n{process.stderr.decode("UTF-8")}')

    return process.stdout.decode("UTF-8").strip()
