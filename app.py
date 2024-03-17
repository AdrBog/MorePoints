"""
The main flask app
"""

from flask import Flask, Blueprint, request, render_template, make_response, redirect, send_file, jsonify, session
from io import BytesIO, StringIO
from datetime import datetime
import ftplib
import re
import json
import secrets
import socket

from utils.ftp import *
from utils.config import *
from utils.conn import *
from utils.misc import *
from utils.msg import *
from utils.tools import tools

app = Flask(__name__)
config = readJSON(f"{CONFIG_DIR}/{CONFIG_FILE}")

#app.secret_key = secrets.token_hex()
app.secret_key = b'SECRET'  # FOR DEV ONLY
app.register_blueprint(tools)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ver=VERSION, points=list_points())

@app.route('/enter_point', methods=['GET', 'POST'])
def enter_point():
    point = request.args.get('point', default="")
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        point = request.form.get('point')
        password = request.form.get('password')
        
        if not os.path.exists(f"{POINTS_CONFIG_DIR}/{point}.point"):
            return render_template('enter_point.html', point=point, hostname=socket.gethostname(), errormsg=Error.POINT_NOT_FOUND)
        
        pointfile = readJSON(f"{POINTS_CONFIG_DIR}/{point}.point")
        
        if password != pointfile["Point"]['Password']:
            return render_template('enter_point.html', point=point, hostname=socket.gethostname(), errormsg=Error.WRONG_PASSWORD)
        
        session[point] = point
        return redirect(f"/point/{point}")
    return render_template('enter_point.html', point=point, hostname=socket.gethostname())

@app.route('/exit/<id>')
def exit_point(id):
    session.pop(id, None)
    return redirect(f'/enter_point?point={id}')

@app.route('/point/<id>', methods=['GET'])
def point(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')

    d = request.args.get('d', default="")
    search = request.args.get('search', default="")
    onlydir = request.args.get('onlydir', default="")
    
    if d == '/': 
        d = ""

    try:
        if search:
            files = list_dir_filter(id, d, r".*" + re.escape(search) + r".*")
        else:
            files = list_dir(id, d)
    except Exception as error:
        return display_error_page(error)

    files = [f for f in files if not f[0] in [".", ".."]]

    for file in files:
        #file[0] = file[0].strip("/")
        file[1]["ext"] = file[0].split(".")[-1].lower()
        try:
            file[1]["modify"] = file[1].get("modify", "0.0").split('.')[0]
            file[1]["modtime"] = datetime.strptime(file[1]["modify"], '%Y%m%d%H%M%S').strftime("%m/%d/%Y, %H:%M:%S")
        except:
            file[1]["modtime"] = file[1]["modify"]
        file[1]["h_size"] = human_readable_size(file[1].get("size", 0))

    return render_template('point.html', pwd=f'{d}', point=id, files=files, search=search, ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])

@app.route('/open/<id>', methods=['GET'])
def openF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    extension = filename.split(".")[-1]
    for key in config.get("OpenWith", []):
        if extension in key["extensions"]:
            return redirect(f"/tools/{key['tool']}/{id}?path={path}&filename={filename}")
    try:
        return send_file(BytesIO(read_file(id, f"{path}/{filename}")), download_name=filename)
    except Exception as error:
        return display_error_page(error)


@app.route('/read/<id>', methods=['GET'])
def readF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    response = make_response(read_file(id, f"{path}/{filename}"), 200)
    response.mimetype = "text/plain"
    return response

@app.route('/edit/<id>', methods=['GET'])
def editF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    extension = filename.split(".")[-1]
    for key in config.get("EditWith", []):
        if extension in key["extensions"]:
            return redirect(f"/tools/{key['tool']}/{id}?path={path}&filename={filename}")
    return redirect(f"/tools/{config.get('DefaultTool', 'text_editor')}/{id}?path={path}&filename={filename}")

@app.route('/download/<id>', methods=['GET'])
def downloadF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    return send_file(BytesIO(read_file(id, f"{path}/{filename}")), download_name=filename, as_attachment=True)

@app.route('/create_folder/<id>', methods=['POST'])
def createFolder(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    filename = request.json.get('filename')
    return create_folder(id, path, filename)

@app.route('/create_file/<id>', methods=['POST'])
def createF(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    filename = request.json.get('filename')
    content = request.json.get('content', "")
    edit = request.json.get('edit', "0")
    output = create_file(id, path, filename, content)
    if edit == "1":
        return jsonify(status="Info", output=Info.FILE_SAVED)
    else:
        return output

@app.route('/delete/<id>', methods=['POST'])
def deleteF(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    filename = request.json.get('filename')
    return delete_file(id, path, filename)

@app.route('/rename/<id>', methods=['POST'])
def renameF(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    new_path = request.json.get('new_path', path)
    filename = request.json.get('filename')
    new_name = request.json.get('new_name', filename)
    return rename_file(id, path, new_path, filename, new_name)

@app.route('/upload/<id>', methods=['POST'])
def uploadF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.form.get('path', '/')
    files = request.files.getlist("file")
    upload_file(id, path, files)
    return redirect(f"/point/{id}?d={path}", code=302)

@app.route('/exec/<id>', methods=['POST'])
def execute(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    commands = request.json.get('commands', [])
    ftp = connect(id)
    try:
        for command in commands:
            output = ftp.sendcmd(command)
        ftp.close()
        return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))


