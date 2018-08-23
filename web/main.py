# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
import requests,json
import os,subprocess
import re

app = Flask(__name__)

#首頁
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        cmd = request.form.get('inputCommand')
        return render_template('index.html', result = execute(cmd))
#CMD
def execute(cmd):
    if cmd == 'help':
        return '這是模擬Linux系統的快來玩'
    if cmd == '新生茶會':
        return '來喝茶~~~'
    if cmd == '黑客社':
        return '打雜的'
    if cmd == '社課':
        return '不用來啦'
    
    x = re.findall("py", cmd)
    try:
        if x[0] == "py":
            return '你再說什麼?'
    except:
        pass

    commands = ['echo','man', 'ping', 'which', 'uname', 'stat', 'head', 'ls', 'id', 'who', 'tail', 'whereis', 'cat', 'pstree']
    cmd_array = cmd.split(' ')
    
    for i in commands:
        if cmd_array[0] == i:
            p = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            r = ">> \n"
            try:
                stdout, stderr = p.communicate(timeout=3)
                if stdout:
                    r += stdout.decode("utf-8")
                if stderr:
                    r += stderr.decode("utf-8")
            except:
                r+="command timeout"
            return r
    return '你再說什麼?'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,threaded=True)