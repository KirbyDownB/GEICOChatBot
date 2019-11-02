from flask import Flask, escape, request, jsonify
from recommender import RecommenderHelper
import random

app = Flask(__name__)
r = RecommenderHelper()
r.load_links()

@app.route('/')
def index():
    return f'Hello!'

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if 'ids' not in data:
        return jsonify({ 'success': False, 'message': 'ids field required' })
    imdb_ids = [int(x[2:]) for x in data['ids']]
    ret = []
    for imdb_id in imdb_ids:
        if imdb_id not in r.imdb2mid:
            continue
        ret.append(r.imdb2mid[imdb_id])
    # Simulate recommendation for now
    return jsonify({ 'success': True, 'ids': random.sample(r.imdb2mid.keys(), 10) })
    # mids = [r.imdb2mid[x] for x in imdb_ids]
