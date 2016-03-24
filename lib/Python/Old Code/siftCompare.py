import numpy as np
import cv2

img2 = cv2.imread("LectureSlide.png") #train image
sift = cv2.SIFT()
kp2, des2 = sift.detectAndCompute(img2,None)
bf = cv2.BFMatcher()

THRESHOLD = 0.75

for i in range(1,12):
	img1 = cv2.imread("can{0}.png".format(i))
	kp1, des1 = sift.detectAndCompute(img1,None)

	#BFMatcher with default params
	matches = bf.knnMatch(des1,des2, k=2)

	# Apply ratio test
	good = []
	for m,n in matches:
		if m.distance < THRESHOLD*n.distance:
			good.append(m.distance)

	print("can{0}.png".format(i))
	print("Num Matches = {0}".format(len(good)))
	print

matches = bf.knnMatch(des1, des1, k=2)
good = []
for m,n in matches:
	if m.distance < THRESHOLD*n.distance:
		good.append(m.distance)

print("self match")
print("Num Matches = {0}".format(len(good)))
print


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