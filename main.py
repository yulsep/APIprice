from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app, origins='*')


@app.route('/course_price', methods=['POST'])
@cross_origin()
def get_course_price():
    url = request.json['url']
    r = requests.get(url)
    html = r.text
    doc = BeautifulSoup(html, 'html.parser')
    price_element = doc.select_one('[data-purpose="course-price-text"]')
    if price_element:
        return jsonify({'url': url, 'price': price_element.text.strip()})
    else:
        return jsonify({'url': url, 'price': 'No se encontró información de precio.'})


if __name__ == '__main__':
    app.run()

