# -*- coding: utf-8 -*-
from flask import Flask, request, render_template,session
import requests,json
import os,subprocess
import re
import sqlite3,base64,string,random

#loging
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=str(os.path.dirname(os.path.abspath(__file__)))+"/access.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

app = Flask(__name__)
app.config.from_object('config')
def key_make(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
app.secret_key = key_make()
#底下放FB給的token
FB_TOKEN = app.config["FB_TOKEN"]
LINE_TOKEN = app.config["LINE_TOKEN"]
WORD = app.config["WORD"]

## log db
db = sqlite3.connect(str(os.path.dirname(os.path.abspath(__file__)))+'/log.db', check_same_thread=False)
c = db.cursor()
@app.route('/wowo', methods=['GET', 'POST'])
def wowo():
    
    if 'admin' not  in session  or session['admin']!="123ojp":
        if request.method == 'POST' and request.form.get('inputCommand') == "@@@":
            session['admin']='123ojp'
            return render_template('tooall.html',result="登入成功 請廣播")
        return render_template('tooall.html',result="請登入")



    if request.method == 'GET':
        return render_template('tooall.html',result="請廣播")

    elif request.method == 'POST':
        list = db.execute("SELECT ID,DATA  from NOTE")
        cmd = request.form.get('inputCommand')
        message = json.loads(json.dumps({"text":cmd}))
        for data in list:
            print (base64.b64decode(data[1]).decode('utf-8'),message,data[0])
            logging.info("廣播:"+base64.b64decode(data[1]).decode('utf-8')+","+cmd+","+str(data[0]))
            sendText(base64.b64decode(data[1]).decode('utf-8'),message,data[0])

        return render_template('tooall.html', result = "成功")


# LINE
def sendText(user, text,bot_count):
    LINE_API = 'https://api.line.me/v2/bot/message/multicast'
    CHANNEL_SERECT ='Bearer {"'+LINE_TOKEN[bot_count]+'"}'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': CHANNEL_SERECT
    }
    if "pic" in text:
            data = {
                "to": [user],
                "messages":[
                {
                    "type":"image",
                    "originalContentUrl": text['pic'][0],
                    "previewImageUrl": text['pic'][1]
                }
                ]
            }
            r = requests.post(LINE_API, headers=headers,json=data)

    data = {
        "to": [user],
        "messages":[
        {
            "type":"text",
            "text":text['text']
        }
        ]
    }

    if "button" in text:
        button_base={"quickReply":{
            "items": [
            ]
              }}


        for button in text['button']:
            button_data= {
                            "type": "action",
                            "action": {
                              "type": "message",
                              "label": button,
                              "text": button
                              }
                            }
            button_base['quickReply']['items'].append(button_data)
        data['messages'][0].update(button_base)
    else:
        button_base={"quickReply":{
            "items": [
            ]
              }}


        for button in app.config["DEFAULT_BUTTON"]:
            button_data= {
                            "type": "action",
                            "action": {
                              "type": "message",
                              "label": button,
                              "text": button
                              }
                            }
            button_base['quickReply']['items'].append(button_data)
        data['messages'][0].update(button_base)
    r = requests.post(LINE_API, headers=headers,json=data)
@app.route('/Line/<path>', methods=['GET','POST'])
def Line(path):
    bot_count=0
    try:
        bot_count=int(path)
    except:
        return ""
    if request.method == 'POST' :
        #try:
            decoded = request.get_json()
            print (decoded)
            logging.info(decoded)
            user = decoded['events'][0]['source']['userId']
            if decoded['events'][0]['type']=="follow":
                sendText(user,message_find("歡迎"),bot_count)
                try:
                    list1 = db.execute("SELECT ID,DATA  from NOTE WHERE ID = '"+path+"'  and DATA = '"+base64.b64encode(user.encode()).decode('utf-8')+"';").fetchall()
                    if len(list1) == 0:
                        c.execute("INSERT INTO  NOTE (ID,DATA) \
                            VALUES ('"+path+"', '"+base64.b64encode(user.encode()).decode('utf-8')+"' )");
                        db.commit()
                except:
                    pass
                return ''
            if decoded['events'][0]['type']!="message" or  decoded['events'][0]['message']['type']!="text":
                return ""
            text= decoded['events'][0]['message']['text']


        #    print "使用者："+str(user.encode('utf-8'))
            sendText(user,message_find(text),bot_count)
            return ''
        
       # except:
            print ("可能是貼圖")
            return ""
    else:
        return 'error'




#FBbot
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

# 訊息
def message_find(text):
    if text in WORD:
        message = WORD[text]
    else:
        message = json.loads(json.dumps({"text":execute(text)}))
    return message

#CMD
def execute(cmd):
    if cmd == 'help':
        message =  '這是模擬Linux系統的快來玩'
    if cmd == '新生茶會':
        message =  '來喝茶~~~'
    if cmd == '黑客社':
        message =  '打雜的'
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
                        r+="command timeout"
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
                    r+="command timeout"
                return r
    else:
        return '你在說什麼?'

#web頁面
@app.route('/web', methods=['GET','POST'])
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
    app.run(host='0.0.0.0',port=8000,threaded=True)


## {u'events': [{u'replyToken': u'c350ec1b4da34aa5b761e83ba41ea6ac', u'type': u'follow', u'timestamp': 1535111480072, u'source': {u'type': u'user', u'userId': u'Ucbe5e9ede37346c1249f04276698b564'}}]}
