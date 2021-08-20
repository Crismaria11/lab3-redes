'''
Universidad del Valle de Guatemala
Redes - 2021
main.py

Roberto Figueroa 18306
Luis Quezada 18028
Esteban del Valle 18221
'''

from module import *
from RoutingTable import *

assignedNode = 'A'

topo = infoGetter(assignedNode,'topo.txt')
print(topo)

names = infoGetter(assignedNode,'names.txt')
print(names)