"""
This is the module where custom tools are stored. For example, the text editor
"""
from flask import Blueprint, redirect, request, render_template, session
from .conn import *
from .misc import *
import json

tools = Blueprint('tools', __name__)

@tools.route('/tools/text_editor/<id>', methods=['GET'])
def text_editor(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    full_path = f"{path}/{filename}"
    try:
        return render_template("tools/text_editor.html", point=id, path=path, filename=filename, text=read_file(id, full_path).decode(), ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])
    except Exception as error:
        print(error)
        return "Can't edit binary file"

@tools.route('/tools/point_editor/<id>', methods=['GET'])
def point_editor(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
        
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    point = request.args.get('filename', default="")
    full_path = f"{path}/{filename}"
    try:
        config = json.loads(read_file(id, full_path).decode())
    except:
        config = {}
    return render_template('tools/point_editor.html', 
        point=point[0:-6],
        point_details=config,
        settings_info=readJSON(f"{POINT_CONFIG_MAP}"),
        config=config.get('Point', {}),
        point_admin=id,
        path=path,
        filename=filename,
        ver=VERSION,
        addons=updateAddons()
        )

@tools.route('/tools/test_tool/<id>', methods=['GET'])
def test_tool(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    full_path = f"{path}/{filename}"
    return render_template("tools/test_tool.html", point=id, path=path, filename=filename, ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])

@tools.route('/tools/link/<id>', methods=['GET'])
def link(id):
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    link = read_file(id, f"{path}/{filename}").decode()
    return redirect(link)
