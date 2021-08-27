'''
Universidad del Valle de Guatemala
Redes - 2021
DVR.py

Roberto Figueroa 18306
Luis Quezada 18028
Esteban del Valle 18221
'''

from slixmpp.basexmpp import BaseXMPP
from node import Node

from asyncio import sleep
from aioconsole import aprint
from time import time
from xml.etree import ElementTree as ET
import json
import asyncio
import numpy as np
from scipy.sparse.csgraph import shortest_path

"""
---------
|   A   |
|  Sec. |
|  Age  |
---------
| B | 0.3 |
| E | 0.5 |
---------
"""

EXPIRATION = 5

class DVR(Node):
    
    def __init__(self, jid, password, entity, asoc_nodes = None):
        super().__init__(jid, password)
        self.DVR_seqnum = 0
        self.DVR = {}
        self.entity = entity
        self.basexmpp = BaseXMPP()
        self.neighbors = asoc_nodes #should be a dict
        self.neighbors_niknames = self.neighbors.keys() if self.neighbors != None else []
        self.topo = {}
        self.all_nodes = [self.entity]
        self.ady_matrix = []
        self.prev_matrix = []
        self.build_topo_package()

    def send_hello(self, hto, hfrom):
        """
        Function for neighbor discovery
        """
        self.send_message(hto, 
            "<hello>", 
            mfrom=hfrom)
        print("Sending hello to neighbor ...")

    def eco(self, eco_to, eco_from):
        """
        Function for measure cost between neighbors
        """
        # print("Sending eco to {}".format(eco_to))
        self.send_message(
            mto=eco_to,
            mbody="<eco time='%f'></eco>" % time(),
            mfrom=eco_from
        )
        

    def build_topo_package(self):
        """
        Function for package build about the network
        """
        self.DVR['node'] = self.entity
        self.DVR['seq'] = self.DVR_seqnum
        self.DVR['age'] = None
        self.DVR['weights'] = {}
        for node in self.neighbors_niknames:
            self.DVR['weights'][node] = 10 # means that they are unavailable
        self.topo[self.DVR['node']] = self.DVR
        

    def update_topo_package(self, node, weight):
        """
        Function for package weights update+
        """
        self.DVR['weights'][node] = weight



    def send_topo_package(self, to):
        """
        Send the topo package to neighbors
        """
        self.DVR_seqnum += 1
        self.DVR['seq'] = self.DVR_seqnum
        self.DVR['age'] = time()
        self.topo[self.DVR['node']] = self.DVR
        dvr_json = json.dumps(self.DVR)
        self.send_message(to, 
            "<pack dvr='%s'></pack>" % dvr_json,
            mfrom=self.boundjid,
        )
        
    
    def recieve_topo_package(self, nfrom, topo_package):
        """
        Recieve topo package from a neighbor,
        this function must process the timestamp and
        the sequence number in order to drop or send
        package
        """
        return "This should be a message stanza"

    def shortest_path(self):
        """
        Must be a Bellman-Ford algorithm implementation
        """
        path = []
        return path.reverse()



    async def update_tables(self):
        while True:
            for router in self.neighbors_niknames:
                self.eco(self.neighbors[router], self.boundjid)
            
            await asyncio.sleep(5)
            # print("Sending packages to neighbors ... ")
            for router in self.neighbors_niknames:
                self.send_topo_package(self.neighbors[router])

    def get_nickname(self, jid):
        key_list = list(self.neighbors.keys())
        val_list = list(self.neighbors.values())

        return key_list[val_list.index(jid)]


    def init_listener(self):
        self.loop.create_task(self.update_tables())

    def flood(self, to, package):
        
        self.send_message(to, 
            "<pack dvr='%s'></pack>" % package,
            mfrom=self.boundjid,
        )

    def save_prev_matrix(self):
    	self.prev_matrix = self.ady_matrix

    def update_ady_matrix(self):
    	self.save_prev_matrix()
        length = len(self.all_nodes)
        self.ady_matrix = np.zeros((length, length),dtype=np.float16)
        for row_node in self.all_nodes:
            for col_node in self.topo[row_node]['weights'].keys():
                row = self.all_nodes.index(row_node)
                col = self.all_nodes.index(col_node)
                self.ady_matrix[row][col] = self.topo[row_node]['weights'][col_node]
        
        # compare tables, update if diff with Bellman Ford
        optimized_matrix = shortest_path(self.ady_matrix,directed=True,method='BF',return_predecessors=False)
        if np.allclose(self.ady_matrix,optimized_matrix) == False:
            self.ady_matrix = optimized_matrix

    def bellmanFord(self, destiny):
        D, Pr = shortest_path(self.ady_matrix,directed=True,method='BF',return_predecessors=True)
        _from = self.all_nodes.index(self.entity)
        path = [destiny]
        k = destiny



    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            if msg['body'][:7] in ("<hello>"):
                msg.reply(self.boundjid).send()
                print("Recieved hello from neighbor, sending answer ...")
            elif msg['body'][1:4] == "eco":
                xml_parse = ET.fromstring(msg['body'])
                timestamp = xml_parse.attrib['time']
                msg.reply("<a_eco time='%s'></a_eco>" % timestamp).send()
            elif msg['body'][1:6] == "a_eco":
                pack_from = msg['from'].bare
                node_entity = self.get_nickname(pack_from)
                end_time = time()
                msg_parse = ET.fromstring(msg['body'])
                start_time = float(msg_parse.attrib['time'])
                delta_time = (end_time - start_time) / 2
                delta_time = round(delta_time, 1)
                self.update_topo_package(node_entity, delta_time)
            elif msg['body'][1:5] == "pack":
                # p_from = msg['from'].bare
                # n_entity = self.get_nickname(p_from)
                parse = ET.fromstring(msg['body'])
                pack_json = parse.attrib['dvr']
                dvr = json.loads(pack_json)
                n_entity = dvr['node']
                if dvr['node'] not in self.topo.keys(): #means that is a new neighbor node, save it and resend (flood)
                    self.topo[dvr['node']] = dvr
                    for neighbor in self.neighbors_niknames:
                        if neighbor != n_entity:
                            self.flood(self.neighbors[neighbor], json.dumps(dvr))
                    if dvr['node'] not in self.all_nodes:
                        self.all_nodes.append(dvr['node'])
                        self.all_nodes.sort()
                    self.update_ady_matrix()
                    
                else: #check if it is not a new topo package
                    d_time = abs(float(self.topo[dvr['node']]['age']) - float(dvr['age']))
                    if self.topo[dvr['node']]['seq'] >= dvr['seq']: #already taken
                        if d_time > EXPIRATION:
                            print("[X] dropping package because is old", dvr['node'] ,dvr['seq'])
                            pass #drop the package
                        

                    else:
                        self.topo[dvr['node']] = dvr # update topo
                        # apply flooding, sends package to child nodes except
                        # node that the package comes from
                        for neighbor in self.neighbors_niknames:
                            if neighbor != n_entity:
                                self.flood(self.neighbors[neighbor], json.dumps(dvr))
                        self.update_ady_matrix()
                print("This is topo for now: ", self.ady_matrix)

            else:
                pass
