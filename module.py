
import json

def jsonToDict(path):
	with open(path) as json_file:
		return json.load(json_file)

def infoGetter(node,path):
	info = jsonToDict(path)
	if info['type'] == 'topo':
		return info['config'][node]
	elif info['type'] == 'names':
		return info['config']
	else:
		return -1