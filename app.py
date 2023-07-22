from flask import Flask
from importlib import import_module
import os

def import_modules(app):
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    for module_file in os.listdir(modules_dir):
        if module_file.endswith('.py') and module_file != '__init__.py':
            module_name = module_file[:-3]
            module = import_module(f'modules.{module_name}')
            module.setup(app)
            print(f'Imported module: {module_name}')

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

import_modules(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('server.crt', 'server.key'))