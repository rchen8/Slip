import json
import os
import subprocess
import shlex
import shutil
import numpy as np
import cv2
import os
import os.path
import imp
try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageEnhance
import pytesseract
import sys
import math
import pipes
import errno

THRESHOLD = 0.6
SCALE = 0.25


DROP_OFF = 0.25
MAX_FRAMES = 10



#slideFolder = "LectureSlides"
#frameFolder = "keyframes"

HOMENAME = "SLIP"
FRAME_FOLDER = "lib/downloads/frames"
VIDEO_LOCATION = "lib/downloads/video.mp4"
SLIDE_LOCATION = "lib/downloads/slide.pdf"
SLIDE_FOLDER = "lib/downloads/slides"

def fileNameToStr(filename):
	    try:
	        image = Image.open(filename)
	        image.thumbnail((512,512))
	        #contrast = ImageEnhance.Contrast(image)
	        #image = contrast.enhance(2)

	        if len(image.split()) == 4:
	            # In case we have 4 channels, lets discard the Alpha.
	            # Kind of a hack, should fix in the future some time.
	            r, g, b, a = image.split()
	            image = Image.merge("RGB", (r, g, b))
	    except IOError:
	        sys.stderr.write('ERROR: Could not open file "%s"\n' % filename)
	        exit(1)
	    return pytesseract.image_to_string(image)

def findStarts(slideFolder, frameFolder):
	

	def resize(img, target):
		smaller = min(img.shape[:2])
		factor = 1.0
		while smaller > target:
			smaller /= 2
			factor /= 2
		return cv2.resize(img, (0,0), fx = factor, fy = factor)


	#http://rosettacode.org/wiki/Longest_common_subsequence#Python
	def lcs(a, b):
	    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
	    # row 0 and column 0 are initialized to 0 already
	    for i, x in enumerate(a):
	        for j, y in enumerate(b):
	            if x == y:
	                lengths[i+1][j+1] = lengths[i][j] + 1
	            else:
	                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
	    # read the substring out from the matrix
	    result = 0
	    x, y = len(a), len(b)
	    while x != 0 and y != 0:
	        if lengths[x][y] == lengths[x-1][y]:
	            x -= 1
	        elif lengths[x][y] == lengths[x][y-1]:
	            y -= 1
	        else:
	            assert a[x-1] == b[y-1]
	            result = 1 + result
	            x -= 1
	            y -= 1
	    return result

	def textCompare(slideText, frameText):
		lcsLength = lcs(slideText, frameText)
		if len(frameText) != 0:
			return lcsLength*math.sqrt((len(slideText)+0.0)/len(frameText))
		else:
			return 0



	def findFileNumber(fileName):
		first,second = fileName.split('.')
		s = ''
		for i in reversed(range(len(first))):
			if not first[i].isdigit():
				break
			else:
				s = first[i] + s
		return int(s)

	allSlides = os.listdir(slideFolder)
	allSlides = filter(lambda x: x[0] != '.', allSlides)
	#print len(allSlides)
	#print allSlides
	allSlides = filter(lambda x: os.path.splitext(x)[1] == '.jpg', allSlides)
	allSlides.sort(key = findFileNumber)
	allFrames = os.listdir(frameFolder)
	allFrames = filter(lambda x: x[0] != '.', allFrames)
	#print len(allFrames)
	allFrames = filter(lambda x: os.path.splitext(x)[1] == '.png', allFrames)
	allFrames.sort(key = findFileNumber)

	numFrames = len(allFrames)
	numSlides = len(allSlides)
	#print numFrames, numSlides




	print("Preprocess Step")
	#sift = cv2.SIFT()
	frameFeatures = []
	frameText = []
	for frameFile in allFrames:
		sift = cv2.SIFT()
		img = cv2.imread(os.path.join(frameFolder, frameFile))
		#print img.shape
		img = resize(img, 200)
		#print img.shape
		frameFeatures.append(sift.detectAndCompute(img, None)[1])
		print(len(frameFeatures))
		#print os.path.join(frameFolder, frameFile)
		frameText.append(fileNameToStr(os.path.join(frameFolder, frameFile)))
		#print frameText[-1]
	print("Frames done")

	slideFeatures = []
	slideText = []
	for slideFile in allSlides:
		sift = cv2.SIFT()
		img = cv2.imread(os.path.join(slideFolder, slideFile))
		#print img.shape
		img = resize(img, 500)
		#print img.shape
		slideFeatures.append(sift.detectAndCompute(img, None)[1])
		#print os.path.join(slideFolder, slideFile)
		print(len(slideFeatures))

		slideText.append(fileNameToStr(os.path.join(slideFolder, slideFile)))
	print("Slides done")



	'''
	def bestFrame(matchQuality):
		matchQuality.sort(key = lambda x: -x[0])
		#print(matchQuality)
		bestFrames = [matchQuality[0]]
		for frame in matchQuality[1:MAX_FRAMES+1]:
			if frame[0] > (1-DROP_OFF) * bestFrames[-1][0]:
				bestFrames.append(frame)
			else:
				break
		topMatch = bestFrames[0][0]
		bestFrames.sort(key = lambda x: x[1])
		currentBegin = -2
		last = -2
		for frame in bestFrames:
			if frame[1] - last > 1:
				currentBegin = frame[1]
			last = frame[1]
			if frame[0] == topMatch:
				return currentBegin


	#bf = cv2.BFMatcher()
	'''

	frameNumbers = []
	grid = []
	for slide in slideFeatures:
		grid.append([])
		matchQuality = []
		for i, frame in enumerate(frameFeatures):
			bf = cv2.BFMatcher()
			matches = bf.knnMatch(frame,slide,k=2)
			numMatches = 0
			for m,n in matches:
				if m.distance < THRESHOLD * n.distance:
					numMatches += 1
			matchQuality.append((numMatches,i+1))
			grid[-1].append(numMatches)

		frameNumbers.append(matchQuality)
		print(len(frameNumbers))




	#print("sqrt")
	def normalize(l):
		x = max(l)
		if x == 0:
			return
		for i in range(len(l)):
			l[i] = (0.0 + l[i])/x

	#print "no normalize"

	def allBestFrames(grid):
		for i in range(len(grid)):
			normalize(grid[i])
		numFrames = len(grid[0])
		numSlides = len(grid)
		pointers = []
		score = []
		for i in range(len(grid)):
			pointers.append([])
			score.append([0]*len(grid[i]))
			for j in range(len(grid[i])):
				pointers[-1].append(j)
		#print(pointers)

		currentRow = 0
		score[0][0] = grid[0][0]
		for i in range(1, numFrames):
			if score[0][i-1] >= grid[0][i]:
				score[0][i] = score[0][i-1]
				pointers[0][i] = pointers[0][i-1]
			else:
				score[0][i] = grid[0][i]
		#print score

		for row in range(1, numSlides):
			starting = row
			score[row][starting] = score[row-1][starting-1] + grid[row][starting]
			for col in range(row+1, numFrames):
				newScore = score[row-1][col-1] + grid[row][col]
				if score[row][col-1] >= newScore:
					score[row][col] = score[row][col-1]
					pointers[row][col] = pointers[row][col-1]
				else:
					score[row][col] = newScore

		answers = []
		currentFrame = pointers[-1][-1]
		answers.append(currentFrame)
		currentRow = numSlides - 1
		while currentRow != 0:
			currentRow -= 1
			currentFrame = pointers[currentRow][currentFrame-1]
			answers.append(currentFrame)

		x = list(reversed(answers))
		return x

	def addText(grid, slideMiddles, slideText, frameText):
		for i, line in enumerate(grid):
			if i < 2:
				lower = 0
			else:
				lower = slideMiddles[i-2]
			if i >= len(slideMiddles) - 2:
				higher = len(grid[0]) - 1
			else:
				higher = slideMiddles[i+2]
			textMatches = []
			print lower, higher
			for frame in range(lower, higher+1):
				#print(i, frame)
				textMatches.append(textCompare(slideText[i], frameText[frame]))
			normalize(textMatches)
			for frame in range(lower, higher+1):
				grid[i][frame] += textMatches[frame-lower]
				grid[i][frame] /= 2

	def matchMiddle(grid, slideMiddles):
		thresh = 0.2
		firstSlideAmount = grid[0][slideMiddles[0]]*thresh
		start = slideMiddles[0]
		while start > 0 and grid[0][start-1] >= firstSlideAmount:
			start -= 1

		endSlideAmount = grid[-1][slideMiddles[-1]]*thresh
		end = slideMiddles[-1]
		while end < len(grid[0]) - 1 and  grid[-1][end+1] >= endSlideAmount:
			end += 1

		dividers = []
		for i in range(len(grid) - 1):
			bestDiv = None
			bestMetric = -1
			for posDiv in range(slideMiddles[i], slideMiddles[i+1]):
				metric = 0
				for slide in range(slideMiddles[i], posDiv+1):
					metric += grid[i][slide]
				for slide in range(posDiv+1, slideMiddles[i+1]+1):
					metric += grid[i+1][slide]
				if metric > bestMetric:
					bestMetric = metric
					bestDiv = posDiv
			dividers.append(bestDiv)

		borders = []
		borders.append([start, dividers[0]])
		for i in range(len(dividers) - 1):
			borders.append([dividers[i] + 1, dividers[i+1]])
		borders.append([dividers[-1]+1, end])
		return borders


	firstList = allBestFrames(grid)

	for i,line in enumerate(firstList):
		print(i+1, line)

	addText(grid, firstList, slideText, frameText)
	finalList = allBestFrames(grid)
	for i,line in enumerate(finalList):
		print(i+1, line)
	borders = matchMiddle(grid, finalList)
	for i,line in enumerate(borders):
		print(i+1, line)

	answer = []
	for i in borders:
		answer.append(i[0])
	return answer


slideFolder = 'SlideFolder'

def findFileNumber(fileName):
	first,second = fileName.split('.')
	s = ''
	for i in reversed(range(len(first))):
		if not first[i].isdigit():
			break
		else:
			s = first[i] + s
	return int(s)

#timestamps = []
frameFolder = FRAME_FOLDER
def get_keyframes(videoLocation, frameFolder):
	timestamps = []
	#os.chdir("Uploads")
	#for root, dirs, files in os.walk(os.path.join(os.getcwd())):
		#for file in files:
	#		print file
	#		print videoLocation
			#if os.path.join("Uploads",file) == videoLocation: #file.endswith('.mp4'):
	moveToHome()
	#file = videoLocation
	filename = videoLocation.split('/')[-1]
	newdir = frameFolder#+ '-frames'
	#global frameFolder
	#frameFolder = newdir
	print newdir
	if (os.path.exists(frameFolder) == False):
		try:
			os.mkdir(frameFolder)
		except OSError as exc:
			if exc.errno != errno.EEXIST:
				raise exc
			pass
	os.chdir(frameFolder)
	with open('output-' + filename + '.txt', 'w') as out:
		cmd = "ffmpeg -i " + pipes.quote(os.path.join(HOME,videoLocation))+ " -vf select='eq(pict_type\,PICT_TYPE_I)' -vsync passthrough -s 320x180 -f image2 %03d.png -loglevel debug 2>&1 | grep select:1"
		print os.getcwd()
		print cmd
		p = subprocess.Popen(cmd, shell=True, stdout=out)
		p.wait()
		out.flush()
	file = open('output-' + filename + '.txt', 'r')	
	#rows = file.readlines()
	with open('timestamps-' + filename + '.txt', 'w') as f:
		for line in file:
			time = line.split(' t:')[1].split(' ')[0]
			#print time
			timestamps.append(float(time))
			if (timestamps[-1] > 1): timestamps[-1] -= 1
			'''
			info = line.split()
			if (info[5][:5] == "time:"):
				hrs, mins, secs = info[5][5:].split(":")
				hr = hrs[-2:] * 60 * 60 * 1000
				mi = mins * 60 * 1000
				sec = secs * 1000
				t = hr + mi + sec
				print t
				timeStamps.append(float(t))
				f.write(t + '\n')
			if (info[5][:2] == "t:"):
				print info[5][2:]
				timestamps.append(float(info[5][2:]))
				f.write(info[5][2:] + '\n')'''
			#if (info[5][:2] == "t:"):
			#	print info[5][2:]
			#	timestamps.append(float(info[5][2:]))
				#f.write(info[5][2:] + '\n')
	print timestamps
	return timestamps

def generateJSON(times, slideFolder):
	timestamp_counter = 0 # dummy variable
	i = 0
	frames = []
	for file in sorted(os.listdir(slideFolder), key = findFileNumber):
		name, ext = os.path.splitext(file)
		if ext == '.jpg':
			slide_obj = {}
			frames.append(slide_obj)
			frames[i]['image'] = os.path.join(file)
			frames[i]['timestamp'] = times[i]
			timestamp_counter += 1
			i += 1
	with open('data.json', 'w') as data:
		json.dump(frames, data, indent=4, sort_keys=True)


def passSlides(slideLocation):
	with open("slideLocation.txt",'w') as f:
		f.write(slideLocation)


'''
Changes the working directory to the home of slip
'''
HOMENAME = "Slip"
def moveToHome():
	while os.path.split(os.getcwd())[-1] != HOMENAME:
		os.chdir("..")
	return os.getcwd()

HOME = moveToHome()



def findFrames(slideLocation, videoLocation, slideFolder, frameFolder):
	'''print '1'
	#f = open('slideLocation.txt', 'r')
	#slideLocation = f.read()
	#f.close()
	print '2'
	print location.split('.')[1]
	print location
	if location.endswith('pdf'):
		print('4')
		with open("slideLocation.txt",'w') as f:
			f.write(location)
		print('5')
		print 'returning'
		return ''
	print '3'
	f = open('slideLocation.txt', 'r')
	slideLocation = f.read()
	f.close()
	videoLocation = location
	print '4'''

	moveToHome()


	timestamps = get_keyframes(videoLocation, frameFolder)
	print len(timestamps)
	
	#os.chdir("..")
	#os.chdir("..")
	#extractSlides(slideLocation)
	moveToHome()
	if (os.path.exists(slideFolder) == False):
		os.makedirs(slideFolder)
	moveToHome()
	print os.getcwd()

	shutil.move(slideLocation, slideFolder)#os.path.join(SLIDE_FOLDER, os.path.split(SLIDE_LOCATION)[-1]))
	os.chdir(slideFolder)
	p = subprocess.Popen("convert {0} a.jpg".format(slideLocation.split('/')[-1]), shell = True)
	p.wait()
	moveToHome()
	shutil.move(os.path.join(slideFolder, os.path.split(slideLocation)[-1]), slideLocation)
	
	frames = findStarts(slideFolder, frameFolder)
	print frames, timestamps
	times = list(timestamps[i] for i in frames)
	generateJSON(times, slideFolder)
	slideLocations = "\\slides"
	with open('data.json', 'r') as data:
		x= data.read()
		#print x
		return x
#	return json.dumps({"timeStamps" : timeStamps, "slideLocations" : slideLocations})



#print findFrames(SLIDE_LOCATION, VIDEO_LOCATION, SLIDE_FOLDER, FRAME_FOLDER)




