from asset import Asset
from packaging import version
from typing import Optional
import cardanocli
import pquery

class Nft:
    def __init__(self, nft_id: int, policy_id: str, asset_name: str, metadata_json: str):
        self.nft_id = nft_id
        self.policy_id = policy_id
        self.asset_name = asset_name
        self.metadata_json = metadata_json

    def __str__(self):
        return f'Nft {{ NftId: {self.nft_id}, PolicyId: {self.policy_id}, AssetName: {self.asset_name}, MetadataJson: {self.metadata_json} }}'

    def __repr__(self):
        return str(self)

def insert(policy_id: str, asset_name: str, metadata_json: str):
    nft_id = pquery.write_and_get_id(f"""
        INSERT INTO nfts (policyId, assetName, metadataJson)
        VALUES ('{policy_id}', '{asset_name}', '{metadata_json}')
        RETURNING nftId;
    """)
    print(nft_id)

    return Nft(nft_id, policy_id, asset_name, metadata_json)

def nft_to_asset(nft: Nft, amount = 1) -> Asset:
    if cardanocli.get_cli_version() >= version.Version("1.32.1"):
        hexAssetName = nft.asset_name.encode("UTF-8").hex()
        name = f"{nft.policy_id}.{hexAssetName}"
    else:
        name = f"{nft.policy_id}.{nft.asset_name}"

    return Asset(name, amount)

def get_nft(nft_id: int) -> Optional[Nft]:
    r = pquery.read(f'''
        SELECT nftId, policyId, assetName, metadataJson
        FROM nfts
        WHERE nftId = {nft_id}
    ''')

    if len(r) == 0:
        # NFT not found
        return None

    r = r[0]
    return Nft(r[0], r[1], r[2], r[3])

def get_nft_from_asset(asset: Asset) -> Optional[Nft]:
    asset_parts = asset.name.split('.')
    search_policy_id = asset_parts[0]
    search_asset_name = '' if len(asset_parts) == 1 else asset_parts[1]
    if cardanocli.get_cli_version() >= version.Version("1.32.1"):
        search_asset_name = bytes.fromhex(search_asset_name).decode("UTF-8")

    search_asset_name = search_asset_name.replace("'", "''")
    r = pquery.read(f'''
        SELECT nftId, policyId, assetName, metadataJson
        FROM nfts
        WHERE policyId = '{search_policy_id}'
            AND assetName = '{search_asset_name}'
    ''')

    if len(r) == 0:
        # NFT not found
        return None

    r = r[0]
    return Nft(r[0], r[1], r[2], r[3])
