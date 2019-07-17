'''
    script to scrape all images of wizards
'''

import time
import shutil
import os
import requests
import pandas as pd
from tqdm import tqdm

# last scraping date: 2019-07-17-13-57-16

PREFIX = (
    'https://storage.googleapis.com/'
    'cheeze-wizards-production/'
    '0xec2203e38116f09e21bc27443e063b623b01345a'
)

def get_url(t_id):
    '''Get full image url.'''
    return os.path.join(PREFIX, f'{t_id}.svg')

if __name__ == "__main__":
    df = pd.read_csv(
        '../data/output/token_id.csv'
    )

    with tqdm(total=len(df['tokenId'])) as pbar:
        for token_id in df['tokenId']:
            pbar.update(1)

            url = get_url(token_id)
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(f'../data/output/images/{token_id}.svg', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                print('Bad request!')

            time.sleep(0.4)
