# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import json
from loguru import logger
from random import randint
app = Flask(__name__)


def pick_random_but_different(name, hat):
    index = randint(0, len(hat['tokens']) - 1)
    if hat['tokens'][index].strip().lower() != name:
        return hat['tokens'].pop(index)
    else:
        return pick_random_but_different(name, hat)


@app.route('/', methods=['GET', 'POST'])
def index():
    picked = ''
    with open('hat.json', 'r', encoding='utf-8') as hat_file:
        hat = json.load(hat_file)
    if request.form:
        name = request.form['name'].strip().lower()
        if name in hat['picked']:
            picked = hat['picked'][name]
        else:
            picked = pick_random_but_different(name, hat)
        hat['picked'][name] = picked
        with open('hat.json', 'w', encoding='utf-8') as hat_file:
            print(json.dumps(hat), file=hat_file)
    return render_template('index.html', picked=picked)


if __name__ == '__main__':
    app.run()
