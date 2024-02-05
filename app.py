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
from utils.ftp import *
from utils.misc import *
from utils.msg import *
from utils.tools import tools

app = Flask(__name__)
# TODO: Avoid overwrite files when creating or renaming files

#app.secret_key = secrets.token_hex()
app.secret_key = b'SECRET'  # FOR DEV ONLY
app.register_blueprint(tools)

setup_MorePoints()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ver=VERSION, points=list_points())

@app.route('/enter_point', methods=['GET', 'POST'])
def enterPoint():
    point = request.args.get('point', default="")
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        point = request.form.get('point')
        password = request.form.get('password')
        
        if not os.path.exists(f"{POINTS_CONFIG_DIR}/{point}.point"):
            return render_template('enter_point.html', point=point, hostname=socket.gethostname(), errormsg=Error.POINT_NOT_FOUND)
        
        readfile = readJSON(f"{POINTS_CONFIG_DIR}/{point}.point")
        
        if password != readfile["FTP"]['Password']:
            return render_template('enter_point.html', point=point, hostname=socket.gethostname(), errormsg=Error.WRONG_PASSWORD)
        
        session[point] = point
        return redirect(f"/point/{point}")
    return render_template('enter_point.html', point=point, hostname=socket.gethostname())

@app.route('/exit/<id>')
def exitPoint(id):
    session.pop(id, None)
    return redirect(f'/enter_point?point={id}')

@app.route('/point/<id>', methods=['GET'])
def point(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')

    d = request.args.get('d', default="")
    search = request.args.get('search', default="")
    if d == '/': 
        d = ""

    ftp = connect(id)
    ftp.cwd(f'{d}')
    files = []
    try:
        data = ftp.mlsd(path="", facts=["type", "size", "perm", "modify"])
        files = [f for f in data]
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise

    for file in files:
        file[1]["ext"] = file[0].split(".")[-1].lower()
        file[1]["modtime"] = datetime.strptime(file[1]["modify"], '%Y%m%d%H%M%S').strftime("%m/%d/%Y, %H:%M:%S")
        try:
            file[1]["h_size"] = human_readable_size(int(file[1]["size"]))
        except:
            pass

    ftp.quit()
    
    files = [f for f in files if not f[0] in [".", ".."]]

    if search:
        regex = re.compile(r".*" + re.escape(search) + r".*")
        filter_search = [f for f in files if regex.match(f[0])]
        files = filter_search
    
    return render_template('point.html', pwd=f'{d}', point=id, files=files, search=search, ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])

@app.route('/open/<id>', methods=['GET'])
def openF(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    extension = filename.split(".")[-1]
    for key in readJSON(f"{CONFIG_DIR}/{CONFIG_FILE}").get("OpenWith", []):
        if extension in key["extensions"]:
            return redirect(f"/tools/{key['tool']}/{id}?path={path}&filename={filename}")
    return send_file(BytesIO(read_file(id, f"{path}/{filename}")), download_name=filename)


@app.route('/read/<id>', methods=['GET'])
def readF(id):
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
    edit_with_list = readJSON(f"{CONFIG_DIR}/{CONFIG_FILE}").get("EditWith", {})
    for key in edit_with_list.get('CustomTools', []):
        if extension in key["extensions"]:
            return redirect(f"/tools/{key['tool']}/{id}?path={path}&filename={filename}")
    return redirect(f"/tools/{edit_with_list.get('DefaultTool', 'text_editor')}/{id}?path={path}&filename={filename}")

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
    ftp = connect(id)
    try:
        output = ftp.mkd(f"{path}/{filename}")
        ftp.close()
        return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))

@app.route('/create_file/<id>', methods=['POST'])
def createFile(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    filename = request.json.get('filename')
    content = request.json.get('content', "")
    edit = request.json.get('edit', "0")
    ftp = connect(id)
    try:
        for file in ftp.nlst(path):
            if file == filename and edit != "1":
                ftp.close()
                return jsonify(status="Error", output=Error.FILE_EXISTS)
        output = ftp.storbinary(f'STOR {path}/{filename}', BytesIO(content.encode()))
        ftp.close()
        if edit == "1":
            return jsonify(status="Info", output=Info.FILE_SAVED)
        else:
            return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))


@app.route('/delete/<id>', methods=['POST'])
def deletef(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    # TODO: Replace path, with filename and path
    path = request.json.get('path', [])
    ftp = connect(id)
    try:
        try:
            output = ftp.delete(path)
        except Exception:
            output = remove_dir(ftp, path)
        ftp.close()
        return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))

@app.route('/rename/<id>', methods=['POST'])
def rename(id):
    if id not in session:
        return jsonify(status="Error", output=Error.LOGIN_REQUIRED)
    path = request.json.get('path')
    filename = request.json.get('filename')
    new_name = request.json.get('new_name')
    ftp = connect(id)
    for file in ftp.nlst(path):
        if file == new_name:
            ftp.close()
            return jsonify(status="Error", output=Error.FILE_EXISTS)
    try:
        output = ftp.rename(f"{path}/{filename}", f"{path}/{new_name}")
        ftp.close()
        return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error)) 
    

@app.route('/upload/<id>', methods=['POST'])
def upload(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    folder = request.form['d']
    files = request.files.getlist("file")
    ftp = connect(id)
    ftp.cwd(folder)
    for f in files:
        ftp.storbinary('STOR ' + f.filename, f)
    ftp.close()
    return redirect(f"/point/{id}?d={folder}", code=302)

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
