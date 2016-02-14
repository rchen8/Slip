import numpy as np
import cv2
import os
import os.path


THRESHOLD = 0.5


DROP_OFF = 0.25
MAX_FRAMES = 10



slideFolder = "LectureSlides2"
frameFolder = "keyframes2"

allSlides = os.listdir(slideFolder)
allSlides = filter(lambda x: x[0] != '.', allSlides)
allSlides.sort()
allFrames = os.listdir(frameFolder)
allFrames = filter(lambda x: x[0] != '.', allFrames)
allFrames.sort()

print("Preprocess Step")
sift = cv2.SIFT()
frameFeatures = []
for frameFile in allFrames:
	img = cv2.imread(os.path.join(frameFolder, frameFile))
	frameFeatures.append(sift.detectAndCompute(img, None)[1])
	print(len(frameFeatures))
print("Frames done")

slideFeatures = []
for slideFile in allSlides:
	img = cv2.imread(os.path.join(slideFolder, slideFile))
	slideFeatures.append(sift.detectAndCompute(img, None)[1])
	print(len(slideFeatures))
print("Slides done")


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


bf = cv2.BFMatcher()

frameNumbers = []
grid = []
for slide in slideFeatures:
	grid.append([])
	matchQuality = []
	for i, frame in enumerate(frameFeatures):
		matches = bf.knnMatch(frame,slide,k=2)
		numMatches = 0
		for m,n in matches:
			if m.distance < THRESHOLD * n.distance:
				numMatches += 1
		matchQuality.append((numMatches,i+1))
		grid[-1].append(numMatches)

	frameNumbers.append(matchQuality)
	print(len(frameNumbers))


for line in grid:
	print line
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