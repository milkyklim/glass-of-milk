'''
    function
'''

import json
import pickle
import requests
from web3.auto.infura import w3
# from tqdm import tqdm

# this info is coming from etherscan
# https://etherscan.io/address/0x2f4bdafb22bd92aa7b7552d270376de8edccbc1e
CW_ADDRESS = '0x2F4Bdafb22bd92AA7b7552d270376dE8eDccbc1E'
CW_BLOCK = 7779141

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


if __name__ == "__main__":
    abi = get_contract_abi(CW_ADDRESS)
    print('got abi')
    contract = w3.eth.contract(CW_ADDRESS, abi=abi)
    print('got contract')

    # this works on the local node
    # logs = contract.events.WizardSummoned().getLogs(fromBlock=CW_BLOCK)
    # this one works with infura
    # logs = []
    # for start in tqdm(range(CW_BLOCK, w3.eth.blockNumber, 1000)):
    #     end = min(start + 1000, w3.eth.blockNumber)
    #     logs.extend(contract.events.WizardSummoned().getLogs(fromBlock=start, toBlock=end))
    # this one for loading data
    logs = pickle.load(open('wiz.pickle', 'rb'))
    
    for k in logs:
        print(k['args']['element'], k['args']['power'])
