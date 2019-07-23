'''
    function to save all token ids to dataframe
'''

import json
import os
import pickle
import requests
from web3.auto.infura import w3
import pandas as pd
from tqdm import tqdm

# this info is coming from etherscan
# https://etherscan.io/address/0x2f4bdafb22bd92aa7b7552d270376de8edccbc1e
CW_ADDRESS = '0x2F4Bdafb22bd92AA7b7552d270376dE8eDccbc1E'
CW_BLOCK = 7779141

ELEMENT_WIZARD = {
    1 : 'ELEMENT_NEUTRAL',
    2 : 'ELEMENT_FIRE',
    3 : 'ELEMENT_WIND',
    4 : 'ELEMENT_WATER',
}
MAX_ELEMENT = 4

DATAPATH = '../data'

def get_contract(address, overwrite=False):
    '''Get contract interface and cache it'''
    filepath = os.path.join(DATAPATH, 'input', 'contract', f'{address}.json')
    if overwrite or not os.path.exists(filepath):
        # cache the response
        abi = get_contract_abi(address)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(abi, f, ensure_ascii=False, indent=4)
    with open(filepath) as f:
        abi = json.load(f)
    return w3.eth.contract(address, abi=abi)

def get_contract_abi(address):
    '''Get contract interface from Etherscan'''
    resp = requests.get(
        'http://api.etherscan.io/api',
        params={'module': 'contract', 'action': 'getabi', 'format': 'raw', 'address': address},
    )
    resp.raise_for_status()
    try:
        return resp.json()
    except json.JSONDecodeError:
        return None

def get_wizards(contract, overwrite=False):
    '''Get all summoned wizards'''
    w_filename = 'wizards.pickle'
    filepath = os.path.join(DATAPATH, 'input', w_filename)
    if overwrite or not os.path.exists(filepath):
        # works on local node
        # wizards = contract.events.WizardSummoned().getLogs(fromBlock=CW_BLOCK)
        # works on infura
        wizards = []
        step = 1000
        for start in tqdm(range(CW_BLOCK, w3.eth.blockNumber, step)):
            end = min(start + step - 1, w3.eth.blockNumber)
            wizards.extend(
                contract.events.WizardSummoned().getLogs(
                    fromBlock=start, 
                    toBlock=end,
                )
            )
        with open(filepath, 'ab') as f:
            pickle.dump(wizards, f)                      
    wizards = pickle.load(open(filepath, 'rb'))
    return wizards

def get_counts(wizards):
    '''Count number of elements'''
    total = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }

    for w in wizards:
        element = w['args']['element']
        total[element] += 1
        
    for i in range(1, MAX_ELEMENT + 1):
        print(f'{ELEMENT_WIZARD[i]}: {total[i]}')  

    print(f'TOTAL: {sum(total.values())}')

def get_all_ids(wizards):
    df = pd.DataFrame(
        data={
            'tokenId': [w['args']['tokenId'] for w in wizards], 
        },
    )
    return df


if __name__ == "__main__":
    contract = get_contract(CW_ADDRESS)
    print('got contract')
    wizards = get_wizards(contract)
    print('got wizards')

    get_counts(wizards)
    df_ids = get_all_ids(wizards)

    df_ids.sort_values(by=['tokenId']).to_csv(
        '../data/output/token_id.csv',
        index=False,
    )
