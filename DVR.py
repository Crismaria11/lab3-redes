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
    
    def __init__(self, jid, password, entity, asoc_nodes = None, t_keys = None):
        super().__init__(jid, password)
        self.DVR_seqnum = 0
        self.DVR = {}
        self.entity = entity
        self.basexmpp = BaseXMPP()
        self.neighbors = asoc_nodes #should be a dict
        self.neighbors_niknames = self.neighbors.keys() if self.neighbors != None else []
        
        self.topo = []
        self.all_nodes = [self.entity]
        self.ady_matrix = []
        self.prev_matrix = []
        self.build_topo_package()

        # ---------
        self.topo_vector = t_keys.sort()

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
            mbody="<eco time='%f' ></eco>" % time(),
            mfrom=eco_from
        )
        

    def build_topo_package(self):
        """
        Function for package build about the network
        destination | dist | next hop
        """
        for i in self.topo_keys:
            if i == self.entity:
                self.topo.append((i , 0, None))
            self.topo.append((i , float('inf'), None))
        

    def update_topo_package(self, node, weight):
        """
        Function for package weights update+
        """

        for i in self.topo:
            if i[0] == node:
                i[1] = weight



    def send_topo_package(self, to):
        """
        Send the topo package to neighbors
        """
        dvr_json = json.dumps(self.topo)
        self.send_message(to, 
            "<pack dvr='%s' from='%s'></pack>" % (dvr_json, self.entity),
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
                if col_node in self.all_nodes:
                    col = self.all_nodes.index(col_node)
                else:
                    return
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


    def parse_path(self, path):
        return [self.all_nodes[i] for i in path]
    
    def get_shortest_path(self, destiny): #should be a character
        _from = self.all_nodes.index(self.entity)
        destiny = self.all_nodes.index(destiny)
        path = [destiny]
        k = destiny
        while self.ady_matrix[_from, k] != -9999:
            path.append(self.ady_matrix[_from, k])
            k = self.ady_matrix[_from, k]
        return self.parse_path(path[::-1]) 
    

    def send_msg(self, to, msg): # to should be a character
        path = self.get_shortest_path(to)
        print("%s: my best path: %s" %(self.entity,path))
        if len(path) > 1:
            self.send_message(
                mto=self.neighbors[path[1]],
                mbody="<msg chat='%s' to='%s' ></msg>" %(msg, to),
                mfrom=self.boundjid
            )


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
                n_entity = parse.attrib['from']
                
            
            elif msg['body'][1:4] == "msg":
                msg_parse = ET.fromstring(msg['body'])
                bare_msg = msg_parse.attrib['chat']
                msg_to = msg_parse.attrib['to']
                if msg_to != self.entity:
                    self.send_msg(msg_to, bare_msg)
                else:
                    print("Incoming message: %s" % bare_msg)
            else:
                pass
