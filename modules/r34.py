from urllib.parse import urlparse, parse_qs
from flask import jsonify, request
import random, requests, cloudscraper

scrape = cloudscraper.create_scraper()

def get_random_post():
    r = scrape.get("https://rule34.xxx/index.php?page=post&s=random")
    return parse_qs(urlparse(r.url).query)["id"][0]

def get_post(post_id):
    r = scrape.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&id={post_id}&json=1')
    data = r.json()[0]
    return {
        'image': data['sample_url'],
        'tags': data['tags'].split(' '),
        'source': data['source'].split(' '),
        'url': f'https://rule34.xxx/index.php?page=post&s=view&id={post_id}'
    }

def get_tag_count(tag):
    r = scrape.get(f'https://rule34.xxx/public/autocomplete.php?q={tag}')
    return int(r.json()[0]['label'].split(' ')[-1][1:-1])

def get_game_entry():
    prev = request.args.get('prev') or ''
    while True:
        id = get_random_post()
        post = get_post(id)
        tag = ''
        for i in range(10):
            tag = random.choice(post['tags'])
            if tag != prev: break
        count = get_tag_count(tag)
        return jsonify({
            'id': id,
            'tag': tag,
            'count': count,
            'image': post['image'],
            'source': post['source'],
            'url': post['url']
        })

def setup(app):
    app.add_url_rule('/r34', 'r34', get_game_entry, methods=['GET'])
    print("Rule34 Routes Loaded")
