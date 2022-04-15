from http import client, server
import os
from flask import Flask, request, jsonify, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
import socket
import struct

app = Flask(__name__)
cors = CORS(app)

def refactor(corenum, EntryAddr, WriteAddr, file):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ip = '10.2.25.123'
    server_port = 1001
    client_socket.connect((server_ip,server_port))
    data = struct.pack("!8s8ss", EntryAddr.encode('utf-8'), WriteAddr.encode('utf-8'), corenum.encode('utf-8'))
    client_socket.send(data)
    for line in file:
        client_socket.send(line)
    state[int(corenum)]['running'] = True
    state[int(corenum)]['task'] = file.filename.split('.')[0]
    print(state[int(corenum)]['running'])
    print(state[int(corenum)]['task'])
    client_socket.close()

def checkArgs(corenum, EntryAddr, WriteAddr, file):
    if corenum == '' or EntryAddr == '' or WriteAddr == '':
        return 0
    if len(corenum) != 1 or len(EntryAddr) != 8 or len(WriteAddr) != 8:
        return 0
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
        print(corenum, EntryAddr, WriteAddr)
        data={'msg': 'ok'}
        return jsonify(data)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    f = request.files.get("file")
    corenum=request.form.get('corenum')
    EntryAddr=request.form.get('EntryAddr')
    WriteAddr=request.form.get('WriteAddr')
    ret = checkArgs(corenum, EntryAddr, WriteAddr, f)
    if ret == 0:
        abort(400)
    if ret == 1:
        abort(500)
    print(corenum, EntryAddr, WriteAddr)
    # refactor(corenum, EntryAddr, WriteAddr, f)
    f.save('/home/hanyi/python-projects/HelloWorld/' + secure_filename(f.filename))
    place = '/home/hanyi/python-projects/HelloWorld/' + secure_filename(f.filename)
    data={'msg': 'refactor success, bin file at ' + place}
    return jsonify(data)

@app.route('/greet/<name>')
def greet (name) :
    return '<hl>Hello, %s</hl＞' % name

if __name__ == '__main__':
    # 监听用户请求
    # 如果有用户请求到来，则执行app的__call__方法
    # app.__call__
    app.run()
    
