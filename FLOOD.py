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
import uuid

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

EXPIRATION = 0.5

class Flood(Node):
    
    def __init__(self, jid, password, entity, asoc_nodes = None):
        super().__init__(jid, password)
        self.LSA_seqnum = 0
        self.LSA = {}
        self.entity = entity
        self.neighbors = asoc_nodes #should be a dict
        self.neighbors_niknames = self.neighbors.keys() if self.neighbors != None else []


        # ----------
        self.recived_msg = []


    def send_msg(self, to, msg):
        for neighbor in self.neighbors_niknames:
            self.send_message(self.neighbors[neighbor], 
            "<flood msg='%s' seq='%s' to='%s' from='%s'></flood>" % (msg, uuid.uuid1(), to, self.entity))
    
    def flood(self, to, msg):
        self.send_message(to, 
            "%s" % msg)

    def init_listener(self):
        pass

    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            if msg['body'][1:6] == "flood":
                # p_from = msg['from'].bare
                # n_entity = self.get_nickname(p_from)
                parse = ET.fromstring(msg['body'])
                _msg = parse.attrib['msg']
                seq = parse.attrib['seq']
                to = parse.attrib['to']
                _from = parse.attrib['from']
                if seq not in self.recived_msg: #means that is a new msg to flood
                    if to != self.entity:
                        print("Flooding message: ", _msg)
                    else:
                        print("%s say: %s" %(_from, _msg))
                    self.recived_msg.append(seq)
                    for neighbor in self.neighbors_niknames:
                        self.flood(self.neighbors[neighbor], msg['body'])
                else:
                    print("Dropping package because has been already sent...")
                    pass
                    
            else:
                pass
