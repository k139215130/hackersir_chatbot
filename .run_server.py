# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, session
import requests, json
import os, subprocess
import re
import base64, string, random

app = Flask(__name__)

app.config.from_object('config')

def key_make(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

app.secret_key = key_make()

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
    
    z = re.findall("db", cmd)
    try:
        if z[0] == "db":
            return '你再說什麼?'
    except:
        pass

    commands = ['echo', 'pwd', 'man', 'ping', 'which', 'uname', 'stat', 'head', 'cat', 'ls', 'id', 'who', 'tail', 'whereis', 'pstree']
    cmd_array = cmd.split(' ')

    for i in commands:
        if cmd_array[0] == i:
            if cmd_array[0] == 'cat':
                y = re.findall(".flag", cmd_array[1])
                if y != []:
                    new_array = [cmd_array[0]  ,cmd_array[1]]
                    p = subprocess.Popen(new_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    r = ">> \n"
                    try:
                        stdout, stderr = p.communicate(timeout=3)
                        if stdout:
                            r += stdout.decode("utf-8")
                        if stderr:
                            r += stderr.decode("utf-8")
                    except:
                        r += "command timeout"
                    return r
                else:
                    return '你沒有權限喔~~'
            else:
                p = subprocess.Popen(cmd_array, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                r = ">> \n"
                try:
                    stdout, stderr = p.communicate(timeout=3)
                    if stdout:
                        r += stdout.decode("utf-8")
                    if stderr:
                        r += stderr.decode("utf-8")
                except:
                    r += "command timeout"
                return r
    else:
        return '你在說什麼?'

#web頁面
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        cmd = request.form.get('inputCommand')
        return render_template('index.html', result = execute(cmd))

#隱私權頁面
@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

if __name__ == '__main__':
    app.run(port=8000, threaded=True, debug=True)
