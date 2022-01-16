import requests
import json
import time
from app.utils import config

def upload_file(path: str) -> str:
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    files = { 'file': open(path,'rb') }
    pinata_config = config.config('pinata')
    headers = { 'pinata_api_key': pinata_config['pinata_api_key'], 'pinata_secret_api_key': pinata_config['pinata_secret_api_key'] }

    response = requests.post(url, headers = headers, files = files)
    if response.status_code == 429:
        print("Too many pinata requests. Sleeping for 60 seconds...")
        time.sleep(60)
        return upload_file(path)

    if response.status_code != 200:
        raise Exception(f'Error uploading {path} to pinata.\n{response.text}')

    rjson = json.loads(response.text)
    return rjson['IpfsHash']
