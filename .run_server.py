# -*- coding: utf-8 -*-
from flask import Flask, request
import requests,json
import os,subprocess

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

#底下放FB給的token
FB_TOKEN = app.config["FB_TOKEN"]

#首頁
@app.route('/', methods=['GET','POST'])
def callback():
    if request.method == 'POST' :
        try:
            message_entries = json.loads(request.data.decode('utf8')) #取得json
            message = message_entries['entry'][0]['messaging'][0]['message']['text'] #取得message
        
            print(message)
            print('\n')
        
            message_sender = message_entries['entry'][0]['messaging'][0]['sender']['id'] #取得誰送的id
            send_fb_message(message_sender,message)
            return ''
        except:
            print( json.loads(request.data.decode('utf8')))
            print('\n')
            return''
    else: #地0關驗證
        return str(request.args['hub.challenge'])
		
# 回訊息
def send_fb_message(to, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages'
	
    response_message = json.dumps({"recipient":{"id": to},
                                   "message":{"text":execute(message)}})
    print(response_message)
    req = requests.post(post_message_url,
                    params={"access_token": FB_TOKEN},
                    headers={"Content-Type": "application/json"},
                    data=response_message)

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