from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, origins='*')


@app.route("/api/price", methods=['POST'])
def get_course_price():
    data = request.get_json()
    url = data['url']
    r = requests.get(url)
    html = r.text
    doc = BeautifulSoup(html, 'html.parser')
    price_element = doc.select_one('[data-purpose="course-price-text"]')
    if price_element:
        return jsonify({'url': url, 'price': price_element.text.strip()})
    else:
        return jsonify({'url': url, 'price': 'No price information found.'})


@app.route("/api/price", methods=['OPTIONS'])
def get_course_options():
    return {'status': 200}


if __name__ == '__main__':
    app.run()

