from flask import render_template, request, make_response

def card():
  url = request.args.get('url')
  if url is None:
    return "Missing URL", 400
  title = request.args.get('title', '')
  redirect = request.args.get('redirect', "https://x.com/NobreHD")
  
  response = make_response(render_template('card.html', url=url, title=title, redirect=redirect))
  response.headers["Cache-Control"] = "public, max-age=86400"
  return response

def setup(app):
    app.add_url_rule('/card', 'card', card, methods=['GET'])
    print("Twitter Article Routes Loaded")
