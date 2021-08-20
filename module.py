
import json

def jsonToDict(path):
	with open(path) as json_file:
		return json.load(json_file)

def topoGetter(node,path):
	info = jsonToDict(path)
	return info['config'][node]

def asignGetter(path):
	info = jsonToDict(path)
	return info['config']