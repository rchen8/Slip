import os
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

import sys
sys.path.insert(0, 'Python/')

from master import findFrames

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'mp4'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#1. Deal with separate file types in the upload_file method
#2. access json with dot notation on front end for different slides
#3. call guy's function ocr and get that json and return in response

temp = ""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print request.files
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # directory = ""
            # if temp is "":
            #     temp = '../uploads/' + filename
            # else:
            directory = '../uploads/' + filename

            print directory
            # print temp, directory
            return findFrames(directory)
            # return jsonify({'foo': 'bar'})
            # return redirect(url_for('uploaded_file', filename=filename))
            
            # return data
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/')
def uploaded_file(filename):
    # return "hello world"
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    data = jsonify({'name': 'dddd'}) #get_json_string()
    return data

if __name__ == "__main__":
    app.run()