FRAME_FOLDER = "lib/downloads/frames"
VIDEO_LOCATION = "lib/downloads/video.mp4"
SLIDE_LOCATION = "lib/downloads/slide.pdf"
SLIDE_FOLDER = "lib/downloads/slides"

import lib.Python.master as master

print master.findFrames(SLIDE_LOCATION, VIDEO_LOCATION, SLIDE_FOLDER, FRAME_FOLDER)