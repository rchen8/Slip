import os
from flask import *
from werkzeug import secure_filename
from subprocess import call

app = Flask(__name__, static_url_path='')

def download_files(video_link, slide_link):
	call(['curl', '-o', 'lib/downloads/video.mp4', video_link])
	call(['curl', '-o', 'lib/downloads/slide.pdf', slide_link])

@app.route('/', methods=['GET'])
def load_homepage():
	return app.send_static_file('index.html')

@app.route('/link', methods=['POST'])
def get_links():
	video_link = request.form['video']
	slide_link = request.form['slide']
	if video_link.endswith('.mp4') and slide_link.endswith('.pdf'):
		download_files(video_link, slide_link)
	return redirect('/')

if __name__ == "__main__":
	app.run()