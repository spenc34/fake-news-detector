import nltk
import tldextract
from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
import editdistance
import requests
import bs4

class UrlNGram:
    def __init__(self, urls, n=2):
        self.ngram = MLE(n)
        train_data, padded_sents = padded_everygram_pipeline(n, urls)
        self.ngram.fit(train_data, padded_sents)

    def get_entropy(self, url):
        return self.ngram.entropy(list(url))
        
    def get_perplexity(self, url):
        return self.ngram.perplexity(list(url))

class UrlAnalyzer:
    def __init__(self, popular_urls):
        self.popular = popular_urls

    @staticmethod
    def clean_url(url):
        xtract = tldextract.extract(url)
        return '.'.join(xtract)

    def find_min_edit_distance(self, url):
        dist = float('inf')
        for site in self.popular:
            new_dist = editdistance.eval(self.clean_url(url), site)
            if new_dist < dist:
                dist = new_dist
        return dist

def get_site_info(url):
    """
    return: tuple(number of iframes on page, whether page uses wordpress)
    """
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        page = bs4.BeautifulSoup(response.text, 'lxml')
        iframes = page.find_all(name='iframe')
        return len(iframes), 1 if response.text.find('wp-content') > -1 else 0
    else:
        raise Exception(f'Could not get site info for {url}')
