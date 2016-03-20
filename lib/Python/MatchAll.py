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


THRESHOLD = 0.6
SCALE = 0.25


DROP_OFF = 0.25
MAX_FRAMES = 10



slideFolder = "LectureSlides"
frameFolder = "keyframes"

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
allSlides.sort(key = findFileNumber)
allFrames = os.listdir(frameFolder)
allFrames = filter(lambda x: x[0] != '.', allFrames)
allFrames.sort(key = findFileNumber)

numFrames = len(allFrames)
numSlides = len(allSlides)




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
	frameText.append(fileNameToStr(os.path.join(frameFolder, frameFile)))
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
'''

gridText = []
for slide in slideText:
	gridText.append([])
	for frame in frameText:
		gridText[-1].append(textCompare(slide,frame))

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
	answers.append(currentFrame+1)
	currentRow = numSlides - 1
	while currentRow != 0:
		currentRow -= 1
		currentFrame = pointers[currentRow][currentFrame-1]
		answers.append(currentFrame+1)

	x = list(reversed(answers))
	return x

def addText(grid, slideMiddles, slideText, frameText):
	for i, line in enumerate(grid):
		if i < 2:
			lower = 0
		else:
			lower = slideMiddles[i-2]
		if i >= len(slideMiddles - 2):
			higher = len(slideMiddles[0] - 1)
		else:
			higher = slideMiddles[i+2]
		textMatches = []
		for frame in range(lower, higher+1):
			textMatches.append(textCompare(slideText[i], frameText[frame]))
		normalize(textMatches)
		for frame in range(lower, higher+1):
			grid[i] += textMatches[frame-lower]
			grid[i] /= 2



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



def matchMiddle(grid, slideMiddles):
	thresh = 0.2
	firstSlideAmount = grid[0]*thresh
	start = slideMiddles[0]
	while start > 0 and grid[0][start-1] >= firstSlideAmount:
		start -= 1

	endSlideAmount = grid[-1]*thresh
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

	'''s = 0
	for i in range(len(x)):
		s += grid[i][x[i]]
	return s
def allBestFrames(grid):
	


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
			score[0][i] = grid[0][1]

	for row in range(1, numSlides):
		starting = row
		score[row][starting] = score[row-1][starting-1] = grid[row][starting]
		for col in range(row+1, numFrames):
			newScore = score[row-1][col-1] + grid[row][col]
			if score[row][col-1] >= newScore:
				score[row][col] = score[row][col-1]
				pointers[row][col] = pointers[row][col-1]
			else:
				score[row][col] = newScore

	answers = []
	bestFrame = 0
	bestScore = 0
	for i in range(numFrames):
		if score[numSlides-1][i] > bestScore:
			bestFrame = i
			bestScore = score[numSlides-1][i]
	currentFrame = bestFrame
	answers.append(currentFrame)
	currentRow = numSlides - 1
	while currentRow != 0:
		currentRow -= 1
		currentFrame = pointers[currentRow][currentFrame-1]
		answers.append(currentFrame+1)

	return list(reversed(answers))'''
'''
import random
grid = []
for i in range(4):
	grid.append([])
	for j in range(11):
		grid[-1].append(random.randint(1,9))
	grid[-1].append(9)

for line in grid: print line
numFrames = len(grid[0])
numSlides = len(grid)
print(allBestFrames(grid))'''





'''for line in grid:
	print " ".join(map(lambda x: str(round(x, 2)), line))'''
	#print(len(frameNumbers), frameNumbers[-1])
'''for i,f in enumerate(frameNumbers):
	f.sort(key = lambda x: -x[0])
	print(i+1, bestMatches(f), f[:10])'''

#print frameNumbers




'''


img2 = cv2.imread("Proving2.png") #train image
sift = cv2.SIFT()
kp2, des2 = sift.detectAndCompute(img2,None)
bf = cv2.BFMatcher()

THRESHOLD = 0.6

matchQuality = []
for i in range(1,653):
	num = str(i)
	if len(num) ==1: num = "0" + num

	img1 = cv2.imread("thumbnail_{0}.jpeg".format(num))
	kp1, des1 = sift.detectAndCompute(img1,None)

	#BFMatcher with default params
	matches = bf.knnMatch(des1,des2, k=2)

	# Apply ratio test
	#good = []
	numMatches = 0
	for m,n in matches:
		if m.distance < THRESHOLD*n.distance:
			numMatches+=1
			#good.append(m.distance)

	print(i)
	#print("Num Matches = {0}".format(numMatches))
	#print
	matchQuality.append((numMatches,i))

#matchQuality.sort(key = lambda x: -x[0])

DROP_OFF = 0.25
MAX_FRAMES = 10
def bestFrame(matchQuality):
	matchQuality.sort(key = lambda x: -x[0])
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

print(bestFrame(matchQuality))


print(matchQuality[:20])'''

'''
matches = bf.knnMatch(des1, des1, k=2)
good = []
for m,n in matches:
	if m.distance < THRESHOLD*n.distance:
		good.append(m.distance)

print("self match")
print("Num Matches = {0}".format(len(good)))
print'''


'''
img1 = cv2.imread("VideoCut.png") #query image
img2 = cv2.imread("LectureSlide.png") #train image

sift = cv2.SIFT()

kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

#BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

# Apply ratio test
good = []
for m,n in matches:
	if m.distance < 0.75*n.distance:
		good.append(m.distance)

print("Num Matches = {0}".format(len(good)))
print("Match Quality = {0}".format(np.mean(good)))'''