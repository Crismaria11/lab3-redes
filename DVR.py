'''
Universidad del Valle de Guatemala
Redes - 2021
DVR.py

Roberto Figueroa 18306
Luis Quezada 18028
Esteban del Valle 18221
'''

from RoutingTable import *

class DVR:
	def __init__(self, name):
		self.name = name
		self.routingTable = RoutingTable(name)
		self.links = {}
		self.addLink(name, 0)
		self.splitHorizonOn = False
	
	def rimport(self,neighborTables):
		returnValue = False
		
		for ntable in neighborTables:
			if ntable.name in self.links: # ver que sea vecina
				for v in ntable.vector_list: # update trable con DVR
					vectorDist = v.dist+self.routingTable.getVector(ntable.name).dist # Revisar si ya se tiene la tabla, si no ver si es un camino mas rapido
					if self.routingTable.contains(v.dest):
						if vectorDist < self.routingTable.getVector(v.dest).dist:
							self.routingTable.editRoute(v.dest, vectorDist, ntable.name)
							returnValue = True
					else:
						self.routingTable.addRoute(v.dest, vectorDist, ntable.name)
						returnValue = True
		return returnValue
					
	def addLink(self, routerID, dist):
		self.links[routerID] = dist
		self.routingTable.addRoute(routerID,dist,routerID)
		
	def removeLink(self, routerID):
		del self.links[routerID]
		v = self.routingTable.getVector(routerID)
		if v.first_hop == routerID:
			self.routingTable.delRoute(routerID)

	def getTable(self):
		return self.routingTable
			
	def printTable(self):
		self.routingTable.printTable()
		
	def printTableToX(self, x): # muetra el camino para llegar a X
		self.routingTable.printTableToX(x)