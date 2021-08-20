
import json

def jsonToDict(path)
	with open(path) as json_file:
		return json.load(json_file)
