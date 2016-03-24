import itertools
import random

def bruteForce(grid):
	best = 0
	bestChoices = None
	for choices in itertools.combinations(range(len(grid[0])), len(grid)):
		#print choices
		s = 0
		for i in range(len(grid)):
			s += grid[i][choices[i]]
		#print s
		if s > best:
			best = s
			bestChoices = choices
	print bestChoices
	return best

def allBestFrames(grid):
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




	'''bestFrame = 0
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
		answers.append(currentFrame+1)'''
	print score
	print pointers

	x = list(reversed(answers))
	print x
	s = 0
	for i in range(len(x)):
		s += grid[i][x[i]]
	return s

'''
grid = []
for i in range(5):
	grid.append([])
	for j in range(20):
		grid[-1].append(random.randint(0,100))'''


outGrid = None
for i in range(100):
	grid = []
	for i in range(5):
		grid.append([])
		for j in range(20):
			grid[-1].append(random.randint(0,100))
	x = bruteForce(grid)
	y = allBestFrames(grid)
	outGrid = grid
	print x, y
	if x != y:
		print ("NOOOOOOOOOOO")
		break

