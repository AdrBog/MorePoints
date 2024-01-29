from flask import Flask, Blueprint, request, render_template, make_response, redirect, send_file, jsonify, session
from admin import *
from utils import *
from io import BytesIO, StringIO
from datetime import datetime
import ftplib
import re
import json
import secrets
import socket

app = Flask(__name__)

#app.secret_key = secrets.token_hex()
app.secret_key = b'SECRET'  # FOR DEV ONLY
app.register_blueprint(admin)


VERSION = "0.1.1"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', ver=VERSION)

@app.route('/enter_site', methods=['GET', 'POST'])
def enterSite():
    site = request.args.get('site', default="")
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        site = request.form.get('site')
        password = request.form.get('password')
        
        if not os.path.exists(f"{SITES_CONFIG_DIR}/{site}.site"):
            return render_template('enter_site.html', site=site, hostname=socket.gethostname(), errormsg=MSG_ERROR_SITE_NOT_FOUND)
        
        readfile = readJSON(f"{SITES_CONFIG_DIR}/{site}.site")
        
        if password != readfile["FTP"]['Password']:
            return render_template('enter_site.html', site=site, hostname=socket.gethostname(), errormsg=MSG_ERROR_WRONG_PASSWORD)
        
        session[site] = site
        return redirect(f"/site/{site}")
    return render_template('enter_site.html', site=site, hostname=socket.gethostname())

@app.route('/exit/<id>')
def exitSite(id):
    session.pop(id, None)
    return redirect(f'/enter_site?site={id}')

@app.route('/site/<id>', methods=['GET'])
def site(id):
    if id not in session:
        return redirect(f'/enter_site?site={id}')

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

    files = [f for f in files if not f[0] in [".", ".."]]

    for file in files:
        file[1]["ext"] = file[0].split(".")[-1].lower()
        file[1]["modtime"] = datetime.strptime(file[1]["modify"], '%Y%m%d%H%M%S')
        try:
            file[1]["h_size"] = human_readable_size(int(file[1]["size"]))
        except:
            pass

    if search:
        regex = re.compile(r".*" + re.escape(search) + r".*")
        filter_search = [f for f in files if regex.match(f[0])]
        files = filter_search
    
    ftp.quit()
    return render_template('site.html', pwd=f'{d}', site=id, files=files, search=search, ver=VERSION, addons=updateAddons(), config=read_site_config(id)["Site"])

@app.route('/open/<id>', methods=['GET'])
def openF(id):
    if id not in session:
        return redirect(f'/enter_site?site={id}')
    path = request.args.get('path', default="")
    filename = path.split("/")[-1]
    download = request.args.get('download', default="0")
    open = request.args.get('open', default="0")
    if download == "1":
        return send_file(BytesIO(read_file(id, path)), download_name=filename, as_attachment=True)
    elif open == "1":
        return send_file(BytesIO(read_file(id, path)), download_name=filename)
    else:
        response = make_response(read_file(id, path), 200)
        response.mimetype = "text/plain"
        return response

@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    if id not in session:
        return redirect(f'/enter_site?site={id}')
    filename = request.args.get('fname', default="")
    folder = request.args.get('d', default="")
    path = f"{folder}/{filename}"
    try: 
        return render_template("text_editor.html", site=id, path=path, folder=folder, filename=filename, text=read_file(id, path).decode(), ver=VERSION, addons=updateAddons(), config=read_site_config(id)["Site"])
    except:
        return "Can't edit binary file"

@app.route('/create_folder/<id>', methods=['POST'])
def createFolder(id):
    if id not in session:
        return jsonify(status="Error", output=MSG_ERROR_LOGIN)
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
        return jsonify(status="Error", output=MSG_ERROR_LOGIN)
    path = request.json.get('path')
    filename = request.json.get('filename')
    content = request.json.get('content', "")
    edit = request.json.get('edit', "0")
    ftp = connect(id)
    try:
        for file in ftp.nlst(path):
            if file == filename and edit != "1":
                ftp.close()
                return jsonify(status="Error", output=MSG_ERROR_FILE_EXISTS)
        output = ftp.storbinary(f'STOR {path}/{filename}', BytesIO(content.encode()))
        ftp.close()
        if edit == "1":
            return jsonify(status="Info", output=MSG_INFO_FILE_SAVED)
        else:
            return jsonify(status="Ok", output=output)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))


@app.route('/delete/<id>', methods=['POST'])
def deletef(id):
    if id not in session:
        return jsonify(status="Error", output=MSG_ERROR_LOGIN)
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
        return jsonify(status="Error", output=MSG_ERROR_LOGIN)
    path = request.json.get('path')
    filename = request.json.get('filename')
    new_name = request.json.get('new_name')
    ftp = connect(id)
    for file in ftp.nlst(path):
        if file == new_name:
            ftp.close()
            return jsonify(status="Error", output=MSG_ERROR_FILE_EXISTS)
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
        return redirect(f'/enter_site?site={id}')
    folder = request.form['d']
    files = request.files.getlist("file")
    ftp = connect(id)
    ftp.cwd(folder)
    for f in files:
        ftp.storbinary('STOR ' + f.filename, f)
    ftp.close()
    return redirect(f"/site/{id}?d={folder}", code=302)

@app.route('/exec/<id>', methods=['POST'])
def execute(id):
    if id not in session:
        return jsonify(status="Error", output=MSG_ERROR_LOGIN)
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