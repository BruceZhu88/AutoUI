#!/usr/bin/env python
# @Time
# @Author   : Bruce.Zhu(Jialin)

# -------------------------------------------------------------------------
import subprocess
import AutoUI.app_config as app_config
import simplejson
import traceback
import PIL
from threading import Thread
from flask import Flask, render_template, request, redirect, jsonify, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from PIL import Image
from AutoUI.src.common.Logger import MyLog
from AutoUI.src.common.upload_file import UploadFile
from AutoUI.src.RunCase import *
from AutoUI.src.common.dbHelper import *

log = MyLog("main").get_log()
log.debug('Start server')
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__)
app.config.from_object(app_config)
bootstrap = Bootstrap(app)
socketio = SocketIO(app, async_mode=async_mode)
# socketio.async_mode
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])
IGNORED_FILES = set(['.gitignore'])

PAGE_INFO = {"page": ""}

"""
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello1.html', name=name)
"""


# *********************************************************************************
#                        *Index*
# *********************************************************************************


@app.route('/')
def index():
    PAGE_INFO['page'] = 'home'
    global app_version
    return render_template('index.html', app_version=app_version)


# *********************************************************************************
#                        *Report*
# *********************************************************************************


@app.route('/report/<file_name>')
def report(file_name):
    return render_template('report/'+file_name)

# *********************************************************************************
#                        *Run Test*
# *********************************************************************************


@app.route('/run_test')
def run_test():
    PAGE_INFO['page'] = 'run_test'
    return render_template('RunTest.html')


@app.route('/run_test/load_case', methods=['GET'])
def load_case():
    path = app.config['UPLOAD_FOLDER']
    all_files = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            all_files.append(filename.rsplit('.', 1)[0])
    if len(all_files) == 0:
        return jsonify({})
    return jsonify({'files_name': all_files})


@app.route('/run_test/run_case', methods=['POST'])
def run_case():
    case_name = request.form.to_dict().get('case')
    file_path = './data/uploads/{}.xlsx'.format(case_name)
    case_id = 0
    conn = sqlite3.connect('./data/running_status.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM RUNNING_STATUS ORDER BY ID DESC LIMIT 1")
    for id in cursor:
        case_id = id[0] + 1
    thread = Thread(target=run_test_case, args=(file_path, case_id))
    thread.setDaemon(True)
    thread.start()
    start_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')

    sql = "INSERT INTO RUNNING_STATUS (NAME, STATUS, START_TIME, OVER_TIME, LINK_REPORT) VALUES ('{}','{}','{}','','')"\
        .format(case_name, '10%', start_time)
    c.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})


@app.route('/run_test/get_status', methods=['GET'])
def get_status():
    status = {}
    conn = sqlite3.connect('./data/running_status.db')
    c = conn.cursor()
    sql = "SELECT * FROM RUNNING_STATUS"
    cursor = c.execute(sql)
    for row in cursor:
        status[row[0]] = row
    if len(status) == 0:
        status = ''
    return jsonify({'status': status})
# *********************************************************************************
#                        *File server*
# *********************************************************************************


@app.route('/file_server')
def file_server():
    PAGE_INFO['page'] = 'file_server'
    return render_template('FileServer.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1
    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))
        return True
    except:
        print(traceback.format_exc())
        return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            # filename = secure_filename(files.filename)
            # filename = gen_file_name(filename)
            filename = files.filename
            mime_type = files.content_type
            if not allowed_file(files.filename):
                result = UploadFile(
                    name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")
            else:
                # save file to disk
                uploaded_file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], filename)
                files.save(uploaded_file_path)
                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename)
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)
                # return json for js call back
                result = UploadFile(name=filename, type=mime_type, size=size)
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data/uploads/ directory
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(
            os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]
        file_display = []
        for f in files:
            size = os.path.getsize(os.path.join(
                app.config['UPLOAD_FOLDER'], f))
            file_saved = UploadFile(name=f, size=size)
            file_display.append(file_saved.get_file())
        return simplejson.dumps({"files": file_display})
    return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)


# *********************************************************************************
#                        *Android*
# *********************************************************************************


@app.route('/android')
def android():
    PAGE_INFO['page'] = 'android'
    return render_template('android.html')


@app.route('/android/adb', methods=['POST'])
def adb():
    cmd_id = request.form.to_dict().get("cmd")
    if cmd_id == 'screencap':
        cmd = '&&'.join([get_adb('shell', cmd_id).format('test.png'),
                         get_adb('system', 'file_pull').format('test.png', '1.png')])
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        code = p.stdout.read().decode("GB2312")
    except:
        code = p.stdout.read().decode("utf-8")
    print(code)
    return jsonify({})


if __name__ == '__main__':
    app_setting = load("./config/app.json")
    app_version = app_setting["version"]
    if not app.config["DEBUG"]:
        go_web_page("http://localhost:{}".format(app_setting["port"]))
        print(
            "Server started: http://localhost:{}".format(app_setting["port"]))
    socketio.run(app, host=app_setting["host"], port=app_setting["port"])
    # app.run(host='0.0.0.0', port=5000)
