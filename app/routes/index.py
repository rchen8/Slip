from flask import jsonify, render_template, request, Flask, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'files/before'
ALLOWED_EXTENSIONS = set(['pdf', 'mp4'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def save_file(file_part):
  if file_part not in request.files:
    flash('No file part')
    return redirect(request.url)

  file = request.files[file_part]
  if file.filename == '':
    flash('No selected file')
    return redirect(request.url)

  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + file_part, filename))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    save_file('video')
    save_file('slides')    
    return render_template('index.html')
  else:
    return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
