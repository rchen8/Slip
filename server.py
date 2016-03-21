import os
from flask import *
from werkzeug import secure_filename
from subprocess import call

app = Flask(__name__, static_url_path='')

VIDEO_LOCATION = 'lib/downloads/video.mp4'
SLIDE_LOCATION = 'lib/downloads/slide.pdf'

def download_files(video_link, slide_link):
	call(['curl', '-o', VIDEO_LOCATION, video_link])
	call(['curl', '-o', SLIDE_LOCATION, slide_link])

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