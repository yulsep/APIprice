from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app, origins='*')


@app.route('/check-prices', methods=['POST'])
@cross_origin()
def get_course_price():
    url = request.json['url']
    if not url.startswith('http'):
        return jsonify({'error': 'Invalid URL'}), 400
    try:
        r = requests.get(url)
        r.raise_for_status()
        html = r.text
        doc = BeautifulSoup(html, 'html.parser')
        price_element = doc.select_one('[data-purpose="course-price-text"]')
        if price_element:
            return jsonify({'url': url, 'price': price_element.text.strip()})
        else:
            return jsonify({'url': url, 'price': 'No price information found in the url.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
