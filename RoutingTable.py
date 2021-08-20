'''
Universidad del Valle de Guatemala
Redes - 2021
RoutingTable.py

Roberto Figueroa 18306
Luis Quezada 18028
Esteban del Valle 18221
'''

class RoutingTable:

	vector_list = []
	name = ""
	def __init__(self, name):
		self.vector_list = []
		self.name = name
	
	def addRoute(self, dest, length, firstHop):
		v = Triple(dest, length, firstHop)
		self.vector_list.append(v)
	
	def delRoute(self, dest):
		try:
			v = self.getVector(dest)
			self.vector_list.remove(v)
		except:
			raise ValueError("Not in List")
	
	def editRoute(self, dest, length, firstHop): 
		v = self.getVector(dest)
		v.dist = length
		v.first_hop = firstHop
		
	def contains(self, dest):
		for vector in self.vector_list:
			if vector.dest == dest:
				return True
		return False
	
	def getVector(self, dest):
		for vector in self.vector_list:
			if vector.dest == dest:
				return vector
		return None

	def printTable(self):
		for vector in self.vector_list:
			print(vector.dest +" "+ str(vector.dist)+" "+ vector.first_hop)
	
	#prints the table links that go to router named X	
	def printTableToX(self, x):
		for vector in self.vector_list:
			if vector.dest == x:
				print(vector.dest +" "+ str(vector.dist)+" "+ vector.first_hop)


class Triple:
	
	dist = None
	dest = None
	first_hop = None
	
	def __init__(self, dest,dist, first_hop):
		self.dest = dest
		self.dist = dist
		self.first_hop = first_hop