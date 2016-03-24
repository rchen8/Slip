import json
import slideMatch
import fileProcessing

DEBUG = True

def findFrames(slideLocation, videoLocation, slideFolder, frameFolder):
	"""Processes everything and returns a json

	IMPORTANT: slideFolder and frameFolder should initially be empty

	Args:
		slideLocation - location of slides relative to home (pdf)
		videoLocation - location of the video relative to home (mp4)
		slideFolder - A folder to put the slides in
		frameFolder - A folder to put the frames in

	Returns: 
		JSON array where each element represents one frame containing:
			image -> filename inside frameFolder
			timestampe -> time in the video for that frame
	"""

	#everything in try except so we can see error statements in when run on server
	try:
		if DEBUG:
			print 'Splitting video'
		timestamps = fileProcessing.extractKeyFrames(videoLocation, frameFolder)
		if DEBUG:
			print 'Done splitting video'
			print 'Splitting slides'

		fileProcessing.splitSlides(slideLocation, slideFolder)

		if DEBUG:
			print "Done splitting slides"

		frameNames = fileProcessing.allFilesOfType(frameFolder, '.png')
		slideNames = fileProcessing.allFilesOfType(slideFolder, '.jpg')
		framePositions = slideMatch.match(slideNames, frameNames)

		#print framePositions
		times = list(timestamps[i] for i in framePositions) #now get timestamp for each frame

		frames = [] #making the JSON to return
		#print times
		for i, filename in enumerate(slideNames):
			frameObj = {}
			frameObj['image'] = filename.split('/')[-1] #filename without path
			frameObj['timestamp'] = times[i]
			#print frameObj
			frames.append(frameObj)

		return json.dumps(frames)


	except Exception as inst:
		print inst
		print type(inst)
		print inst.args

		raise inst
