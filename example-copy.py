import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
	djv = Dejavu(config)

	

	# Recognize audio from a file
	song = djv.recognize(FileRecognizer, "mp3/cut-Sean-Fournier--Falling-For-You.mp3")
	print "From file we recognized: %s\n" % song

	
