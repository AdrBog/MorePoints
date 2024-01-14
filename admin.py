from flask import Flask, Blueprint, request, render_template, make_response, redirect, send_file, jsonify, session
from utils import *
import os
import json
import re
import subprocess

admin = Blueprint('admin', __name__)

@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        admin_password = readJSON(f'{CONFIG_DIR}/{CONFIG_FILE}')['Admin']['Password']
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
    sites = []
    search = request.args.get('search', default="")

    for file in os.listdir(SITES_CONFIG_DIR):
        if file.endswith(".site"):
            sites.append(file[0:-5])

    if search:
        regex = re.compile(r".*" + re.escape(search) + r".*")
        filter_search = [f for f in sites if regex.match(f)]
        sites = filter_search

    return render_template('admin/admin.html', sites=sites)

@admin.route('/admin/create_site', methods=['POST'])
def create_site():
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    sitename = request.json.get('sitename')
    try:
        config = generate_site_config()
        config["FTP"]["Root"] = f"{SITES_DIR}/{sitename}"
        config["Permissions"] = {"/": "elradfmwMT"}
        output = writeJSON(f"{SITES_CONFIG_DIR}/{sitename}.site", config)
        if not os.path.exists(f"{SITES_DIR}/{sitename}"):
            os.makedirs(f"{SITES_DIR}/{sitename}")
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))

@admin.route('/admin/delete_site', methods=['POST'])
def delete_site():
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    sitename = request.json.get('sitename')
    try:
        output = os.remove(f"{SITES_CONFIG_DIR}/{sitename}.site")
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))

@admin.route('/admin/edit_site/<id>')
def edit_site(id):
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    return render_template('admin/edit_site.html', 
        site=id, 
        site_details=readJSON(f"{SITES_CONFIG_DIR}/{id}.site"), 
        settings_info=readJSON(f"{SITE_CONFIG_MAP}"),
        config=read_site_config(id)["Site"]
        )

@admin.route('/admin/save_site/<id>', methods=['POST'])
def save_site(id):
    if not request.cookies.get('admin_logged'):
        return redirect('/admin/login')

    json = request.json.get('content')
    try:
        output = writeJSON(f"{SITES_CONFIG_DIR}/{id}.site", json)
        return jsonify(status="Ok", output=output)
    except Exception as error:
        return jsonify(status="Error", output=str(error))
