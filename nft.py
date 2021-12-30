from asset import Asset
from packaging import version
import cardanocli

class Nft:
    def __init__(self, nft_id: str, policy_id: str, asset_name: str, metadata_json: str):
        self.nft_id = nft_id
        self.policy_id = policy_id
        self.asset_name = asset_name
        self.metadata_json = metadata_json

    def __str__(self):
        return f'Nft {{ NftId: {self.nft_id}, PolicyId: {self.policy_id}, AssetName: {self.asset_name}, MetadataJson: {self.metadata_json} }}'

    def __repr__(self):
        return str(self)

def nft_to_asset(nft: Nft) -> Asset:
    if cardanocli.get_cli_version() >= version.parse("1.32.1"):
        hexAssetName = nft.asset_name.encode("UTF-8").hex()
        return Asset(f"{nft.policy_id}.{hexAssetName}", 1)

    return Asset(f"{nft.policy_id}.{nft.asset_name}", 1)
