import pandas as pd
import json
from featureextract import UrlAnalyzer

urls = None
with open('../data/urls.json') as f:
    urls = json.load(f)

df = pd.read_csv('../data/full_data.csv')

fake_urls = [str(url) for url in df[df.target == 1]['url']]
real_urls = [str(url) for url in df[df.target == 0]['url']]
fake_clean = [UrlAnalyzer.clean_url(url) for url in fake_urls]
real_clean = [UrlAnalyzer.clean_url(url) for url in real_urls]

urls['train'] = {
    'fake': {
        'raw': fake_urls,
        'clean': fake_clean
    },
    'real': {
        'raw': real_urls,
        'clean': real_clean
    }
}

with open('../data/urls.json', mode='w') as f:
    json.dump(urls, f)