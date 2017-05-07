from flask import Flask
from flask import render_template
from flask import request, url_for, redirect, flash
from werkzeug.utils import secure_filename
#因为要处理中文问题没有加文件名审查！！！！！！
import os, config
#from os.path import join, dirname, realpath
app = Flask(__name__)
app.config.from_object(config)
#UPLOADS_PATH = join(dirname(realpath(__file__)), 'file/')#后面的字符串是文件路径
#app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
UPLOAD_FOLDER = 'file/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#现在通过app.config["变量名"]，我们可以访问到对应的变量
#一种配置文件
basedir = os.path.abspath(os.path.dirname(__file__))
'''
dirname os.path.realpath(path) 返回path的真实路径
os.path.dirname(__file__)返回脚本的路径
'''
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    #def allow_file(filename):
        #return '.' in filename and \
            #filename.rsplit('.', 1).lower() in ALLOWED_EXTENSIONS

    if request.method== 'POST':
        if 'file' not in request.files:
            flash('not file post')
            return redirect(url_for('index'))
        file = request.files.get('file')
        if file.filename == '':
            flash('No file name', 'error')
            return redirect(url_for('index'))
        # 因为要处理中文问题没有加文件名审查！！！！！！
        #filename = secure_filename(file.filename)
        filename = file.filename
        #file.save(join(app.config['UPLOAD_FOLDER'], filename))
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        #os.path.join是用来拼接路径用
        flash(filename, 'file_size')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
