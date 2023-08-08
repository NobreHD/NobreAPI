from urllib.parse import urlparse, parse_qs
from flask import jsonify, request
import random, requests, cloudscraper,validators, time

scrape = cloudscraper.create_scraper()
log = {}

def get_random_post():
    r = scrape.get("https://rule34.xxx/index.php?page=post&s=random")
    return int(parse_qs(urlparse(r.url).query)["id"][0])

def get_post(post_id):
    r = scrape.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&id={post_id}&json=1')
    data = r.json()[0]
    source = list(filter(lambda x: validators.url(x), data['source'].split(' ')))
    return {
        'image': data['sample_url'],
        'tags': data['tags'].split(' '),
        'source': source,
        'url': f'https://rule34.xxx/index.php?page=post&s=view&id={post_id}'
    }

def get_tag_count(tag):
    r = scrape.get(f'https://rule34.xxx/public/autocomplete.php?q={tag}')
    return int(r.json()[0]['label'].split(' ')[-1][1:-1])

def get_game_entry():
    req_time = time.time()
    if log.get(req_time) != None:
        log[req_time] += 1
    else:
        log[req_time] = 1
    while list(log.keys())[0] < req_time - 60:
        del log[list(log.keys())[0]]
    
    vstag = []
    vsid = []
    if request.method == 'POST':
        data = request.get_json()
        vstag = data['tags']
        vsid = data['ids']
    while True:
        id = get_random_post()
        if id in vsid: continue
        post = get_post(id)
        tag = ''
        for i in range(10):
            tag = random.choice(post['tags'])
            if tag not in vstag: break
        count = get_tag_count(tag)
        return jsonify({
            'id': id,
            'tag': tag,
            'count': count,
            'image': post['image'],
            'source': post['source'],
            'url': post['url']
        })
    
def get_current_requests():
    if log == {}:
        return jsonify({
            'requests': 0
        })
    rq = 0
    while list(log.keys())[0] < req_time - 60:
        del log[list(log.keys())[0]]
    for i in log:
        rq += log[i]
    return jsonify({
        'requests': rq
    })

def setup(app):
    app.add_url_rule('/r34', 'r34', get_game_entry, methods=['GET', 'POST'])
    app.add_url_rule('/r34/requests', 'r34_requests', get_current_requests, methods=['GET'])
    print("Rule34 Routes Loaded")
