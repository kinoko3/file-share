'''
from flask import Flask
from flask import render_template
from flask import request, url_for, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
#因为要处理中文问题没有加文件名审查！！！！！！
import os, config
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
#from os.path import join, dirname, realpath
app = Flask(__name__)
app.config.from_object(config)
#UPLOADS_PATH = join(dirname(realpath(__file__)), 'file/')#后面的字符串是文件路径
#app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
#现在通过app.config["变量名"]，我们可以访问到对应的变量
#一种配置文件
ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']
#dirname os.path.realpath(path) 返回path的真实路径
#os.path.dirname(__file__)返回脚本的路径
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    def allow_file(filename):
        #in是成员运算符，在一个指定的序列中找达到值返回ture，否则返回false
        #not in同上，但是false和ture条件交换
        #\是续行符
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('not file post')
            return redirect(url_for('index'))
        file = request.files.get('file')
        if file.filename == '':
            flash('No file name', 'error')
            return redirect(url_for('index'))
        if file and allow_file(file.filename):
            # 因为要处理中文问题没有加文件名审查！！！！！！
            #filename = secure_filename(file.filename)
            filename = file.filename
            #file.save(join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #os.path.join是用来拼接路径用
            flash(filename, 'file_size')
            return redirect(url_for('index'))
        else:
            flash('文件名错误', 'error')
            return redirect(url_for('index'))
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
'''
import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import config
app = Flask(__name__)
app.config.from_object(config)
app.config['UPLOADED_PHOTOS_DEST'] = app.config['UPLOAD_FOLDER']
#UPLOADED_FILES_DEST = '/path/to/the/uploads'
#如果你的set叫photos，那么这条设置就改成：UPLOADED_PHOTOS_DEST
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片'),#error错误信息
        FileRequired(u'无文件')#验证这个字段有没有文件，一样的error错误信息
    ])
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        flash('文件上传成功')
    else:
        file_url =None
    return render_template('index.html', form=form, file_url=file_url)
if __name__ == '__main__':
    app.run(debug=True)
