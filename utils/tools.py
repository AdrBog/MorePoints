"""
This is the module where custom tools are stored. For example, the text editor

Tools can be set up on <code>config/config.json</code>

Here's an example:

```json
"OpenWith": [
    {
        "extensions": ["lnk", "link"],
        "tool": "link"
    },
    {
        "extensions": ["txt", "msg", "ini", "js", "css", "py", "sh"],
        "tool": "text_editor"
    },
    {
        "extensions": ["point"],
        "tool": "point_editor"
    }
],
"EditWith": [
    {
        "extensions": ["foo", "bar"],
        "tool": "test_tool"
    },
    {
        "extensions": ["point"],
        "tool": "point_editor"
    }
],
"DefaultTool": "text_editor"
```

By default, when you try to edit a file with MorePoints, the text editor will be used by default (Look at key DefaultTool)

But you can specify your own tools (Look at key EditWith)

To access a tool, go to the path: <code>http://{HOST}/tools/{TOOL NAME}/{POINT ID}?path={RESOURCE PATH}&filename={RESOURCE NAME}</code>

"""
from flask import Blueprint, redirect, request, render_template, session
from .conn import *
from .misc import *
import json

# TODO: The module utils.tools can be refactorized

tools = Blueprint('tools', __name__)

@tools.route('/tools/text_editor/<id>', methods=['GET'])
def text_editor(id):
    """
    This tool edits text files
    :param: path: Absolute path of folder where resource is stored
    :param: filename:
    :return: render_template "templates/tools/text_editor.html"
    """
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    full_path = f"{path}/{filename}"
    try:
        return render_template("tools/text_editor.html", point=id, path=path, filename=filename, text=read_file(id, full_path).decode(), ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])
    except UnicodeDecodeError:
        return display_error_page(Exception(Error.EDIT_BINARY_FILE))
    except Exception as error:
        return display_error_page(error)

@tools.route('/tools/point_editor/<id>', methods=['GET'])
def point_editor(id):
    """
    This tool edits points files (*.point)
    :param: path: Absolute path of folder where resource is stored
    :param: filename:
    :return: render_template "templates/tools/point_editor.html"
    """
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
    """
    This tool does nothing, it's only for test purposes
    :param: path: Absolute path of folder where resource is stored
    :param: filename:
    :return: render_template "templates/tools/test_tool.html"
    """
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    full_path = f"{path}/{filename}"
    return render_template("tools/test_tool.html", point=id, path=path, filename=filename, ver=VERSION, addons=updateAddons(), config=read_point_config(id)["Point"])

@tools.route('/tools/link/<id>', methods=['GET'])
def link(id):
    """
    This tool opens link files (*.lnk, *.link)
    :param: path: Absolute path of folder where resource is stored
    :param: filename:
    :return: Redirection to the link inside the link file
    """
    if id not in session:
        return redirect(f'/enter_point?point={id}')
    path = request.args.get('path', default="")
    filename = request.args.get('filename', default="")
    link = read_file(id, f"{path}/{filename}").decode()
    return redirect(link)
