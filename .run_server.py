# -*- coding: utf-8 -*-
from flask import Flask, render_template
import string, random

app = Flask(__name__)

def key_make(size=20, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

app.secret_key = key_make()

#web頁面
@app.route('/')
def index():
    return render_template('index.html')

#隱私權頁面
@app.route('/flag')
def flag():
    return render_template('flag.html')

#隱私權頁面
@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
