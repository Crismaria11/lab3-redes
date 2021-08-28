'''
Universidad del Valle de Guatemala
Redes - 2021
module.py

Roberto Figueroa 18306
Luis Quezada 18028
Esteban del Valle 18221
'''

import json

from numpy import inf

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

def keys(path):
	info = jsonToDict(path)
	return list(info['config'].keys())

