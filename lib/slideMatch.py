import numpy as np
import cv2
try:
  import Image
except ImportError:
  from PIL import Image
import pytesseract
import math
import os

OCR_IMAGE_SIZE = 512
FRAME_IMAGE_SIZE = 200
SLIDE_IMAGE_SIZE = 500

MATCH_THRESHOLD = 0.6


DEBUG = True

def match(slideFileNames, frameFileNames):
  """Matches up slides and frames 
  
  Args:
    slideFileNames -- Generator containing the filename of slide images
    frameFileNames -- Same as above but for frames

  Returns:
    A list containing the frame index that corresponds to each slide
  """

  if DEBUG:
    print "Preprocess Step"

  if DEBUG:
    frameFeatures, frameText = openFiles(frameFileNames, FRAME_IMAGE_SIZE, "frames")
    slideFeatures, slideText = openFiles(slideFileNames, SLIDE_IMAGE_SIZE, "slides")
  else:
    frameFeatures, frameText = openFiles(frameFileNames, FRAME_IMAGE_SIZE)
    slideFeatures, slideText = openFiles(slideFileNames, SLIDE_IMAGE_SIZE)

  if DEBUG:
    print "Preprocess Done"
    print "Creating Grid"

  grid = featureGrid(frameFeatures, slideFeatures)
  if DEBUG:
    print "Grid Done"

  firstList = determineBestFrames(grid)
  if DEBUG:
    print "Preliminary matches done"
    print "Adding information from text"

  addText(grid, firstList, slideText, frameText)
  finalList = determineBestFrames(grid)
  slideBorders = matchMiddle(grid, finalList)
  answer = []
  for border in slideBorders:
    answer.append(border[0])
  
  if DEBUG:
    print "Data processing done"

  return answer



#-------ALGORITHMS-------------------------------------------------------------

def featureGrid(frameFeatures, slideFeatures):
  """Creates a grid of the number of SIFT matches of each pair of frame and slide"""
  grid = []
  count = 0
  for slide in slideFeatures:
    grid.append([])
    matchQuality = []
    for i, frame in enumerate(frameFeatures):
      bf = cv2.BFMatcher()
      matches = bf.knnMatch(frame, slide, k=2)
      numMatches = 0
      for m,n in matches:
        if m.distance < MATCH_THRESHOLD * n.distance:
          numMatches += 1
      matchQuality.append((numMatches,i+1))
      grid[-1].append(numMatches)
    count += 1
    if DEBUG: 
      print "{0}/{1}".format(count,len(slideFeatures))
  return grid

def determineBestFrames(grid):
  """Matches up all the frames and slides in the most effective way possible
  Assumptions:
    Every slide appears only once - yes this is wrong but it works well enough for now
    Every slide appears later in the video then the previous one
  Goal:
    Trace a path from the top of the grid to the bottom. Whenever moving down,
    you must move right some number of steps. Maximize the the sum of this path
  Solution:
    Dynamic Programming - ask Guy if you want help understanding. Hopefully he didn't
              forget how it works
  """

  normalize(grid)
  numFrames = len(grid[0])
  numSlides = len(grid)
  pointers = []
  score = []
  for i in range(len(grid)):
    pointers.append([])
    score.append([0]*len(grid[i]))
    for j in range(len(grid[i])):
      pointers[-1].append(j)


  currentRow = 0
  score[0][0] = grid[0][0]
  for i in range(1, numFrames):
    if score[0][i-1] >= grid[0][i]:
      score[0][i] = score[0][i-1]
      pointers[0][i] = pointers[0][i-1]
    else:
      score[0][i] = grid[0][i]


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

def matchMiddle(grid, slideMiddles):
  """Expands slides to take up a range of values instead of only the middle"""

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

def addText(grid, slideMiddles, slideText, frameText):
  "Adds text matching to the grid"
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
    #print lower, higher
    for frame in range(lower, higher+1):
      #print(i, frame)
      textMatches.append(textCompare(slideText[i], frameText[frame]))
    normalizeRow(textMatches)
    for frame in range(lower, higher+1):
      grid[i][frame] += textMatches[frame-lower]
      grid[i][frame] /= 2


def normalize(grid):
  """normalizes every row in a grid so the maximum is 1
  -----MODIFIES IN PLACE"""
  #print grid
  for row in range(len(grid)):
    maxVal = max(grid[row])
    if maxVal != 0:
      for col in range(len(grid[row])):
        grid[row][col] /= float(maxVal) #prevent issues with integer round down

def normalizeRow(row):
  """Same as above but for one run"""
  maxVal = max(row)
  if maxVal != 0:
    for col in range(len(row)):
      row[col] /= float(maxVal)




#-------FILE UTILITIES---------------------------------------------------------

def openFiles(fileNames, targetSize, debug = None):
  """Opens a list of files and returns SIFT features as well as slide text
  Args:
    fileNames: List of the filenames of images
    targetSize: A scale of how big the image should be after opening
  Returns:
    (features, text)
    features -> list of SIFT features of each image
    text -> OCR text extracted from each image
  """
  if debug is not None:
    print "Starting " + debug


  features = []
  text = []

  count = 0
  for name in fileNames:
    sift = cv2.xfeatures2d.SIFT_create() #TODO: Can this be moved out of the loop for efficiency??
    img = cv2.imread(name)
    img = resize(img, targetSize)
    features.append(sift.detectAndCompute(img, None)[1])
    text.append(fileNameToStr(name))
    count += 1
    if DEBUG:
      print "{0}/{1}".format(count,len(fileNames))

  return (features, text)



def fileNameToStr(filename):
  """Uses tesseract OCR to open an image at filename and return its text"""
  try:
    image = Image.open(filename)
    image.thumbnail((OCR_IMAGE_SIZE, OCR_IMAGE_SIZE))

    if len(image.split()) == 4:
      # In case we have 4 channels, lets discard the Alpha.
      # Kind of a hack, should fix in the future some time.
      r, g, b, a = image.split()
      image = Image.merge("RGB", (r, g, b))
  except IOError:
    sys.stderr.write('ERROR: Could not open file "%s"\n' % filename)
    exit(1)
  return pytesseract.image_to_string(image)

def findFileNumber(fileName):
  """Gives the number at the end of a file fileName

  Example: findFileNumber("a022.pdf") -> 22
  """
  first, second = fileName.split('.')
  s = ''
  for i in reversed(range(len(first))):
    if not first[i].isdigit():
      break
    else:
      s = first[i] + s
  return int(s)




#-------IMAGE UTILITIES--------------------------------------------------------

def resize(img, target):
  """Scales down the an open cv image
  Args:
    img -- an opencv image
    target -- An upperbound on the smaller dimension
  Returns: A scaled down image where the smaller dimension <= target
  """
  smaller = min(img.shape[:2])
  factor = 1.0
  while smaller > target:
    smaller /= 2
    factor /= 2
  return cv2.resize(img, (0,0), fx = factor, fy = factor)

#-------STRING UTILITIES-------------------------------------------------------



def textCompare(slideText, frameText):
  """Returns a metric of how similar the text on a slide and frame are
  Args:
    slideText - text on the slide
    frameText - text on the frame
  Returns: Metric based on longest common subsequence
  """
  lcsLength = lcs(slideText, frameText)
  if len(frameText) != 0: 
    #penalize for just having a ton of frameText
    return lcsLength*math.sqrt((len(slideText)+0.0)/len(frameText))
  else:
    return 0


#source: #http://rosettacode.org/wiki/Longest_common_subsequence#Python
def lcs(a, b):
  """Returns the length of the Longest cd common subsequence of a and b"""
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
