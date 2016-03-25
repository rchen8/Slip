# ffmpeg -i "yourInputVideo.mp4" -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 thumbnail_%02d.jpeg

import os
import subprocess
import shlex


def get_keyframes():
	for root, dirs, files in os.walk(os.path.join(os.getcwd())):
			for file in files:
				if file.endswith('.mp4'):
					filename = os.path.splitext(file)[0]
					newdir = filename + '-frames'
					if (os.path.exists(newdir) == False):
						os.mkdir(newdir)
					os.chdir(newdir)
					with open('output-' + filename + '.txt', 'w') as out:
						cmd = "ffmpeg -i " + "../" + file + " -vf select='eq(pict_type\,PICT_TYPE_I)' -vsync passthrough -s 320x180 -f image2 %03d.png -loglevel debug 2>&1 | grep select:1"
						p = subprocess.Popen(cmd, shell=True, stdout=out)
						p.wait()
						out.flush()
					file = open('output-' + filename + '.txt', 'r')	
					rows = file.readlines()
					with open('timestamps-' + filename + '.txt', 'w') as f:
						for line in rows:
							info = line.split()
							if (info[5][:2] == "t:"):
								f.write(info[5][2:] + '\n')

get_keyframes()