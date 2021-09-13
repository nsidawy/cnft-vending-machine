class Nft:
    def __init__(self, nft_id: str, asset_name: str, metadata_json: str):
        self.nft_id = nft_id
        self.asset_name = asset_name
        self.metadata_json = metadata_json

    def __str__(self):
        return f'Nft {{ NftId: {self.nft_id}, AssetName: {self.asset_name}, MetadataJson: {self.metadata_json} }}'

    def __repr__(self):
        return str(self)

