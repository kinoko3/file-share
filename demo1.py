from flask import Flask
from flask import render_template
from flask import request, url_for, redirect, flash
from werkzeug.utils import secure_filename
import os
#from os.path import join, dirname, realpath
app = Flask(__name__)
#UPLOADS_PATH = join(dirname(realpath(__file__)), 'file/')#后面的字符串是文件路径
#app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
'''
dirname os.path.realpath(path) 返回path的真实路径
os.path.dirname(__file__)返回脚本的路径

'''
UPLOAD_FOLDER = 'file/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method== 'POST':
        if 'file' not in request.files:
            flash('not file post')
            return redirect(url_for('index'))
        file = request.files.get('file')
        if file.filename == '':
            flash('No file name')
            return redirect(url_for('index'))
        filename = secure_filename(file.filename)
        #file.save(join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
