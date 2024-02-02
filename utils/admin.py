from flask import Flask, Blueprint, request, render_template, make_response, redirect, send_file, jsonify, session
import os
import json
import re
import subprocess

from .misc import *
from .config import *

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = readJSON(f'{CONFIG_DIR}/{CONFIG_FILE}')['Admin'].get('Password', 'admin')
        if password == admin_password:
            response = make_response(redirect('/admin'))
            response.set_cookie('admin_logged', 'True')
            return response
        else:
            return render_template("admin/admin_login.html", errormsg=MSG_ERROR_WRONG_PASSWORD)
    return render_template("admin/admin_login.html")

@admin.route('/admin/logout', methods=['GET'])
def admin_logout():
    response = make_response(redirect('/admin/login'))
    response.set_cookie('admin_logged', '', expires=0)
    return response

@admin.route('/admin', methods=['GET'])
def admin_index():
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')
    points = []
    search = request.args.get('search', default="")

    for file in os.listdir(POINTS_CONFIG_DIR):
        if file.endswith(".point"):
            points.append(file[0:-6])

    if search:
        regex = re.compile(r".*" + re.escape(search) + r".*")
        filter_search = [f for f in points if regex.match(f)]
        points = filter_search

    return render_template('admin/admin.html', points=points)

@admin.route('/admin/create_point', methods=['POST'])
def create_point():
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    pointname = request.json.get('pointname')
    try:
        config = generate_point_config()
        config["FTP"]["Root"] = f"{POINTS_DIR}/{pointname}"
        config["Permissions"] = {"/": "elradfmwMT"}
        output = writeJSON(f"{POINTS_CONFIG_DIR}/{pointname}.point", config)
        if not os.path.exists(f"{POINTS_DIR}/{pointname}"):
            os.makedirs(f"{POINTS_DIR}/{pointname}")
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))

@admin.route('/admin/delete_point', methods=['POST'])
def delete_point():
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    pointname = request.json.get('pointname')
    try:
        output = os.remove(f"{POINTS_CONFIG_DIR}/{pointname}.point")
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))

@admin.route('/admin/edit_point/<id>')
def edit_point(id):
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    return render_template('admin/edit_point.html', 
        point=id, 
        point_details=readJSON(f"{POINTS_CONFIG_DIR}/{id}.point"), 
        settings_info=readJSON(f"{POINT_CONFIG_MAP}"),
        config=read_point_config(id)["Point"]
        )

@admin.route('/admin/save_point/<id>', methods=['POST'])
def save_point(id):
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    json = request.json.get('content')
    try:
        output = writeJSON(f"{POINTS_CONFIG_DIR}/{id}.point", json)
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))
