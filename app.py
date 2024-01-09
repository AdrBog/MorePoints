from flask import Flask, request, render_template, make_response, redirect, send_file, jsonify, session
from sites import *
from io import BytesIO, StringIO
from datetime import datetime
import ftplib
import re
import json
import secrets
import socket
import configparser

app = Flask(__name__)

#app.secret_key = secrets.token_hex()
app.secret_key = b'SECRET'  # FOR DEV ONLY
SITES_DIR = "sites"
CONFIG_DIR = "config"
ADDONS_FILE = "addons.json"
VERSION = "0.1.0"

# Messages

MSG_ERROR_LOGIN = "You have to login"
MSG_ERROR_FILE_EXISTS = "File already exists"
MSG_INFO_FILE_SAVED = "File saved"

def updateAddons():
    with open(f"{CONFIG_DIR}/{ADDONS_FILE}") as f:
        return json.load(f)

def connect(id):
    ftp = ftplib.FTP('127.0.0.1')
    with open(f"{CONFIG_DIR}/sites.json", "r") as readfile:
        sites = json.load(readfile)
        ftp.login(id, sites[id]['password'])
    return ftp

def read_file(id, path):
    ftp = connect(id)
    r = BytesIO()
    ftp.retrbinary(f'RETR /{path}', r.write)
    ftp.quit()
    return r.getvalue()

def remove_dir(ftp, path):
    for (name, properties) in ftp.mlsd(path=path):
        if name in ['.', '..']:
            continue
        elif properties['type'] == 'file':
            ftp.delete(f"{path}/{name}")
        elif properties['type'] == 'dir':
            remove_dir(ftp, f"{path}/{name}")
    ftp.rmd(path)

def read_site_config(id):
    parser = configparser.ConfigParser()
    try:
        parser.read_file(StringIO(read_file(id, "siteconf").decode()))
    except:
        parser.read_file(StringIO(""))
    return dict(parser)

def human_readable_size(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

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
        with open(f"{CONFIG_DIR}/sites.json", "r") as readfile:
            sites = json.load(readfile)
            if site not in sites:
                return render_template('enter_site.html', site=site, hostname=socket.gethostname(), errormsg='Site not found')
            elif password != sites[site]['password']:
                return render_template('enter_site.html', site=site, hostname=socket.gethostname(), errormsg='Wrong password')
        session[site] = site
        return redirect(f"/site/{site}")
    return render_template('enter_site.html', site=site, hostname=socket.gethostname())

@app.route('/exit/<id>')
def exitSite(id):
    session.pop(id, None)
    return redirect(f'/enter_site?site={id}')

@app.route('/site/<id>', methods=['GET'])
def site(id):
    if not id in session:
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

    for file in files:
        file[1]["ext"] = file[0].split(".")[-1].lower()
        file[1]["modtime"] = datetime.strptime(file[1]["modify"], '%Y%m%d%H%M%S')
        file[1]["h_size"] = human_readable_size(int(file[1]["size"]))

    if search:
        regex = re.compile(r".*" + re.escape(search) + r".*")
        filter_search = [f for f in files if regex.match(f[0])]
        files = filter_search
    
    ftp.quit()
    return render_template('site.html', pwd=f'{d}', site=id, files=files, search=search, ver=VERSION, addons=updateAddons(), config=read_site_config(id))

@app.route('/open/<id>', methods=['GET'])
def openF(id):
    if not id in session:
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
    if not id in session:
        return redirect(f'/enter_site?site={id}')
    filename = request.args.get('fname', default="")
    folder = request.args.get('d', default="")
    path = f"{folder}/{filename}"
    try: 
        return render_template("text_editor.html", site=id, path=path, folder=folder, filename=filename, text=read_file(id, path).decode(), ver=VERSION, addons=updateAddons())
    except:
        return "Can't edit binary file"

@app.route('/create_folder/<id>', methods=['POST'])
def createFolder(id):
    if not id in session:
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
    if not id in session:
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
        return jsonify(status="Info", output=MSG_INFO_FILE_SAVED)
    except ftplib.all_errors as error:
        ftp.close()
        return jsonify(status="Error", output=str(error))


@app.route('/delete/<id>', methods=['POST'])
def deletef(id):
    if not id in session:
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
    if not id in session:
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
    if not id in session:
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
    if not id in session:
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