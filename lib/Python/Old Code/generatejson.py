import json
import os

def generateJSON():
	frames = []
	timestamp_counter = 0 # dummy variable
	i = 0
	for file in os.listdir('slides'):
		slide_obj = {}
		frames.append(slide_obj) 
		frames[i]['url'] = file
		frames[i]['timestamp'] = timestamp_counter
		timestamp_counter += 1
		i += 1
	with open('data.json', 'w') as data:
		json.dump(frames, data, indent=4, sort_keys=True)

generateJSON()
