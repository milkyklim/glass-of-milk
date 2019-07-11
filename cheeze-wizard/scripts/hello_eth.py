'''
    function
'''

import json
import requests
from web3.auto.infura import w3


def get_contract_abi(address):
    '''
    get_contract_abi
    '''
    resp = requests.get(
        'http://api.etherscan.io/api',
        params={'module': 'contract', 'action': 'getabi', 'format': 'raw', 'address': address},
    )
    resp.raise_for_status()
    try:
        return resp.json()
    except json.JSONDecodeError:
        return None


print(f'Current block: {w3.eth.blockNumber}')
print(f'Current gas price: {w3.eth.gasPrice}')

CW = '0x2F4Bdafb22bd92AA7b7552d270376dE8eDccbc1E'

print(f'Cheeze wizards balance: {w3.eth.getBalance(CW)}')

abi = get_contract_abi(CW)
contract = w3.eth.contract(CW, abi=abi)
