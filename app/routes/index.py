from flask import jsonify, render_template, request, Flask, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
import os

app.config['BEFORE_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'files/before')
app.config['AFTER_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), 'files/after')

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in set(['pdf', 'mp4'])

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
    file.save(os.path.join(app.config['BEFORE_FOLDER'] + '/' + file_part, filename))

# Endpoints

@app.route('/upload', methods=['POST'])
def upload_file():
  save_file('video')
  save_file('slides')    
  return render_template('player.html')

@app.route('/slide', methods=['GET'])
def get_slide():
  return send_from_directory(app.config['AFTER_FOLDER'] + '/slides', request.args.get('filename'))

@app.route('/video', methods=['GET'])
def get_video():
  # TODO - dynamically create filename
  return send_from_directory(app.config['BEFORE_FOLDER'] + '/video', 'video.mp4')

# Templates

@app.route('/player', methods=['GET'])
def player():
  return render_template('player.html')

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')
