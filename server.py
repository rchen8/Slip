import os
from flask import *
from werkzeug import secure_filename
from subprocess import call
import lib.Python.master as master


app = Flask(__name__, static_url_path='')



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

#example parameters
FRAME_FOLDER = "lib/downloads/frames"
VIDEO_LOCATION = "lib/downloads/video.mp4"
SLIDE_LOCATION = "lib/downloads/slide.pdf"
SLIDE_FOLDER = "lib/downloads/slides"

'''
returns JSON string with an array of JSON objects. Each object has:
	image: filename of the slide inside of SLIDE_FOLDER
	timestamp: time in seconds corresponding to the slide
locations should be relative to the Slip folder, as this method automatically moves to that folder
'''
def getTimeStampes(slideLocation, videoLocation, slideFolder, frameFolder):
 return master.findFrames(slideLocation, videoLocation, slideFolder, frameFolder)

if __name__ == "__main__":
	app.run()