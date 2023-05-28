from flask import Flask
import os

def import_modules():
    for module in os.listdir(os.path.dirname(__file__)+"/modules"):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        imp_mod = __import__(f"modules.{module[:-3]}", fromlist=['setup'])
        imp_mod.setup(app)
        print(f"Imported {module[:-3]}")

app = Flask(__name__)

import_modules()
