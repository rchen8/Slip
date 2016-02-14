import numpy as np
import cv2

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
	good = []
	for m,n in matches:
		if m.distance < THRESHOLD*n.distance:
			good.append(m.distance)

	print(i)
	print("Num Matches = {0}".format(len(good)))
	print
	matchQuality.append((len(good),i))

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