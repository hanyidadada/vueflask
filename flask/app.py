from ast import Return
from http import client, server
import io
import os
from tkinter import image_names
from PIL import Image
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
import socket
import struct

app = Flask(__name__)
cors = CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

status ={'1':[{
        'num': '0',
        'state': 'running',
        'task': 'Control Core'  
        },{
        'num': '1',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '2',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '3',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '4',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '5',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '6',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '7',
        'state': 'stopped',
        'task': ''  
        }],
        '2':[{
        'num': '0',
        'state': 'running',
        'task': 'Control Core'  
        },{
        'num': '1',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '2',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '3',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '4',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '5',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '6',
        'state': 'stopped',
        'task': ''  
        },{
        'num': '7',
        'state': 'stopped',
        'task': ''  
        }]}

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径

def refactor(dspnum, corenum, EntryAddr, WriteAddr, file):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip = '10.2.25.123'
    server_port = 1001
    client_socket.connect((server_ip,server_port))
    byte = chr(0x01)
    data = struct.pack("!s8s8sss", byte.encode(), EntryAddr.encode('utf-8'), WriteAddr.encode('utf-8'), dspnum.encode('utf-8'), corenum.encode('utf-8'))
    client_socket.send(data)
    for line in file:
        client_socket.send(line)
    client_socket.close()

def resetcore(dspnum, corenum):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip = '10.2.25.123'
    server_port = 1001
    client_socket.connect((server_ip,server_port))
    byte = chr(0x03)
    data = struct.pack("!ss", byte.encode(), dspnum.encode('utf-8'), corenum.encode('utf-8'))
    client_socket.send(data)

    client_socket.close()

ImageName = '/bmp/result'
id = 1
def getImage(): 
    global id
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip = '10.2.25.123'
    server_port = 1001
    client_socket.connect((server_ip,server_port))
    byte = chr(0x02)
    data = struct.pack("!s", byte.encode())
    client_socket.send(data)
    recv_data = client_socket.recv(4)
    if recv_data != "succ".encode():
        print("查询失败!")
        client_socket.close()
        abort(500)
    recvd_size = 0  # 定义已接收文件的大小
    mkdir("./bmp")
    fp = open(basedir + ImageName + str(id) + '.bmp', 'wb')
    print('start receiving...')
    filesize = 173878
    while not recvd_size == filesize:
        data = client_socket.recv(17838)
        recvd_size += len(data)
        fp.write(data)
    fp.close()
    client_socket.close()

def checkArgs(dspnum, corenum, EntryAddr, WriteAddr, file):
    if dspnum == '' or corenum == '' or EntryAddr == '' or WriteAddr == '':
        return 0
    if len(corenum) != 1 or len(EntryAddr) != 8 or len(WriteAddr) != 8:
        return 0
    if EntryAddr == '00000000':
        return 3
    if file.filename.endswith(".bin") == False:
        return 1
    return 2

@app.route('/sendArgs', methods=['GET', 'POST'])
def home():
    if request.method=='GET':
        corenum=request.args.get('corenum')
        EntryAddr=request.args.get('EntryAddr')
        WriteAddr=request.args.get('WriteAddr')
        if corenum=='':
            data={'msg': 'Check your args!'}
            return jsonify(data)
        data={'msg': 'ok'}
        return jsonify(data)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    f = request.files.get("file")
    dspnum=request.form.get('dspnum')
    corenum=request.form.get('corenum')
    EntryAddr=request.form.get('EntryAddr')
    WriteAddr=request.form.get('WriteAddr')
    ret = checkArgs(dspnum, corenum, EntryAddr, WriteAddr, f)
    if ret == 0:
        abort(400)
    if ret == 1:
        abort(500)
    if ret == 3:
        # resetcore(dspnum, corenum)
        status[dspnum][int(corenum)]['state'] = 'stopped'
        status[dspnum][int(corenum)]['task'] = ''
        data={'msg': 'reset succ'}
        return jsonify(data)
    # refactor(dspnum, corenum, EntryAddr, WriteAddr, f)
    status[dspnum][int(corenum)]['state'] = 'running'
    status[dspnum][int(corenum)]['task'] = f.filename.split('.')[0]
    mkdir("./bin")
    f.seek(0, 0)
    f.save(basedir + '/bin/' + secure_filename(f.filename))
    place = basedir + '/bin/' + secure_filename(f.filename)
    data={'msg': 'refactor success, bin file at ' + place}
    return jsonify(data)

@app.route('/greet/<name>')
def greet (name) :
    return '<hl>Hello, %s</hl＞' % name

@app.route('/getTable', methods=['GET', 'POST'])
def getTable():
    if request.method=='GET':
        dspnum=request.args.get('dspnum')
        if dspnum == '':
            dspnum = '1'
        data={'table': status[dspnum]}
        return jsonify(data)

@app.route('/getPic',methods=['GET', 'POST'])
def getPic():
    global id
    f = getImage()
    img_url = basedir + ImageName + str(id) + '.bmp'
    with open(img_url, 'rb') as f:
        a = f.read()
    img_stream = io.BytesIO(a)
    img = Image.open(img_stream)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='BMP')
    imgByteArr = imgByteArr.getvalue()
    id += 1
    return  imgByteArr



if __name__ == '__main__':
    # 监听用户请求
    # 如果有用户请求到来，则执行app的__call__方法
    # app.__call__
    app.run()
    
