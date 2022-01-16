from typing import List, Tuple

class Asset:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __str__(self):
        return f'{self.amount} {self.name}'

    def __repr__(self):
        return f'Asset {{ Name: {self.name}, Amount: {self.amount} }}'

def get_multi_asset_str(assets: List[Asset]) -> str:
    asset_strings = list(map(lambda a: f'{a.amount} {a.name}', assets))
    return " + ".join(asset_strings)

def get_assets_from_str(multi_asset_str: str) -> List[Asset]:
    asset_strs = multi_asset_str.split("+")
    asset_arrs = [list(filter(None, asset_str.split(" "))) for asset_str in asset_strs]
    assets = []
    for asset_arr in asset_arrs:
        # skip datum
        if len(asset_arr) != 2:
            continue
        assets.append(Asset(asset_arr[1], int(asset_arr[0])))
    return assets

def get_lovelace_and_other_assets(assets: List[Asset]) -> Tuple[Asset, List[Asset]]:
    lovelace_str = "lovelace"
    lovelace_assets = [x for x in assets if x.name.lower() == lovelace_str]
    other_assets = [x for x in assets if x.name.lower() != lovelace_str]
    if len(lovelace_assets) != 1:
        raise Exception(f"List of assets does not contain lovelace {assets}")

    return (lovelace_assets[0], other_assets)
