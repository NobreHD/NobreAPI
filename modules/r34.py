from urllib.parse import urlparse, parse_qs
from flask import jsonify, request
import random, requests, cloudscraper,validators, time

scrape = cloudscraper.create_scraper()

def get_random_post():
    r = scrape.get("https://rule34.xxx/index.php?page=post&s=random")
    return int(parse_qs(urlparse(r.url).query)["id"][0])

def get_post(post_id, streamer_mode):
    r = scrape.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&id={post_id}&json=1')
    data = r.json()[0]
    source = list(filter(lambda x: validators.url(x), data['source'].split(' ')))
    image = data['preview_url'] if streamer_mode else data['sample_url']
    return {
        'image': image,
        'tags': data['tags'].split(' '),
        'source': source,
        'url': f'https://rule34.xxx/index.php?page=post&s=view&id={post_id}'
    }
    
def get_post_new(post_id):
    r = scrape.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&id={post_id}&json=1')
    data = r.json()[0]
    source = list(filter(lambda x: validators.url(x), data['source'].split(' ')))
    source.insert(0, "https://rule34.xxx/index.php?page=post&s=view&id={post_id}")
    return {
        'image': data['sample_url'],
        'censored': data['preview_url'],
        'tags': data['tags'].split(' '),
        'source': source
    }

def get_tag_count(tag):
    try:
        r = scrape.get(f'https://rule34.xxx/public/autocomplete.php?q={tag}')
        return int(r.json()[0]['label'].split(' ')[-1][1:-1])
    except:
        return 0

def try_repeat(func, args, times):
    for i in range(times):
        try:
            return func(*args)
        except Exception as e:
            error = e
            print(e.with_traceback())
            print(f"Error executing function '${func.__name__}', retrying...")

def get_game_entry():
    vstag = []
    vsid = []
    streamer_mode = False
    if request.method == 'POST':
        data = request.get_json()
        vstag = data['tags'] if data.get('tags') != None else []
        vsid = data['ids'] if data.get('ids') != None else []
        streamer_mode = data['streamer_mode'] if data.get('streamer_mode') != None else False
    while True:
        id = get_random_post()
        if id in vsid: continue
        post = try_repeat(get_post, [id, streamer_mode], 10)
        if post.get('tags') == None: continue
        tag = ''
        for i in range(10):
            tag = random.choice(post['tags'])
            if tag not in vstag: break
        count = try_repeat(get_tag_count, [tag], 10)
                
        return jsonify({
            'id': id,
            'tag': tag,
            'count': count,
            'image': post['image'],
            'source': post['source'],
            'url': post['url']
        })
        
def array_trim(arr, length):
    return arr[:min(len(arr), length)]
        
def get_game_entry_new():
    vstag = []
    vsid = []
    if request.method == 'POST':
        data = request.get_json()
        vstag = array_trim(data['tags'], 30).map if data.get('tags') != None else []
        vsid = array_trim(data['ids'], 20) if data.get('ids') != None else []
    
    while True:
        img_id = get_random_post()
        if img_id in vsid: continue
        
        post = try_repeat(get_post_new, [img_id], 10)
        if post.get('tags') == None: continue
        
        tag = ''
        for i in range(10):
            tag = random.choice(post['tags'])
            if tag not in vstag: break
            
        count = try_repeat(get_tag_count, [tag], 10)
        if count == 0: continue
                
        return jsonify({
            'id': img_id,
            'tag': tag,
            'count': count,
            'image': post['image'],
            'censored': post['censored'],
            'source': post['source']
        })

def setup(app):
    app.add_url_rule('/r34', 'r34', get_game_entry, methods=['GET', 'POST'])
    app.add_url_rule('/r34/new', 'r34_new', get_game_entry_new, methods=['GET', 'POST'])
    print("Rule34 Routes Loaded")
