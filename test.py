from celery import Celery
import lib.backend as backend

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

SLIDE_LOCATION = 'files/before/slides/slides.pdf'
VIDEO_LOCATION = 'files/before/video/video.mp4'
SLIDE_FOLDER = 'files/after/slides'
FRAME_FOLDER = 'files/after/frames'

@app.task
def run():
  return backend.findFrames(SLIDE_LOCATION, VIDEO_LOCATION, SLIDE_FOLDER, FRAME_FOLDER)

if __name__ == '__main__':
  from test import run
  result = run.delay()
  while not result.ready():
    pass
  print result.result
