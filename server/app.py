from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from model import FakeNewsNetwork as FNN
from featureextract import UrlNGram, UrlAnalyzer, get_site_info

app = Flask(__name__)
CORS(app)

urls = None
with open('../data/urls.json') as url_file:
    urls = json.load(url_file)

model = FNN(7, 2)
model.load_weights('../data/fake-news-model.pt')

raw_bigram = UrlNGram(urls['train']['fake']['raw'] + urls['train']['real']['raw'])
clean_bigram = UrlNGram(urls['train']['fake']['clean'] + urls['train']['real']['clean'])

analyzer = UrlAnalyzer(urls['popular'])

@app.route('/predict', methods=['POST'])
def predict():
    url = request.json['url']
    clean_url = analyzer.clean_url(url)
    try:
        entropy = raw_bigram.get_entropy(url)
        perplexity = raw_bigram.get_perplexity(url)
        clean_entropy = clean_bigram.get_entropy(clean_url)
        clean_perplexity = clean_bigram.get_perplexity(clean_url)
        edit_distance = analyzer.find_min_edit_distance(url)
        num_iframes, has_wp_content = get_site_info(url)
        tensor = model.dict_to_tensor({
            'entropy': entropy,
            'perplexity': perplexity,
            'clean_entropy': clean_entropy,
            'clean_perplexity': clean_perplexity,
            'edit_distance': edit_distance,
            'num_iframes': num_iframes,
            'has_wp_content': has_wp_content
        })
        probabilities = model(tensor)
        response_body = {
            'probabilityFake': round(float(probabilities[0][1]), 4)
        }
        status_code = 200
    except Exception as e:
        response_body = {
            'message': str(e)
        }
        status_code = 400
    finally:
        response = jsonify(response_body)
        return response, status_code


if __name__ == '__main__':
    app.run(host='localhost', port=3000)