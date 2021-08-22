from slixmpp.basexmpp import BaseXMPP
from node import Node

from asyncio import sleep
from aioconsole import aprint
from time import time
from xml.etree import ElementTree as ET
import json

"""
---------
|   A   |
|  Sec. |
|  Age  |
---------
| B | 4 |
| E | 5 |
---------
"""

class LSR(Node):
    
    def __init__(self, jid, password, entity, asoc_nodes = None):
        super().__init__(jid, password)
        self.LSA_seqnum = 0
        self.LSA = {}
        self.entity = entity
        self.basexmpp = BaseXMPP()
        self.neighbors = asoc_nodes #should be a dict
        self.neighbors_niknames = self.neighbors.keys() if self.neighbors != None else []
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
        self.send_message(
            mto=eco_to,
            mbody="<eco time='%f'></eco>" % time(),
            mfrom=eco_from
        )
        

    def build_topo_package(self):
        """
        Function for package build about the network
        """
        self.LSA['node'] = self.entity
        self.LSA['seq'] = self.LSA_seqnum
        self.LSA['age'] = None
        self.LSA['weights'] = {}
        for node in self.neighbors_niknames:
            self.LSA['weights'][node] = 0

    def update_topo_package(self, node, weight):
        """
        Function for package weights update
        """
        self.LSA['weights'][node] = weight



    def send_topo_package(self, to):
        """
        Send the topo package to neighbors
        """
        lsa_json = json.dumps(self.LSA)
        self.send_message(to, 
            "<pack lsa='%s'></pack>" % lsa_json,
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
        Must be a Dijktra implementation
        """
        path = []
        return path.reverse()



    async def update_tables(self):
        while True:
            await sleep(5)
            print("--------------------->Updateado")


    def init_listener(self):
        self.loop.create_task(self.update_tables())

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
                end_time = time()
                msg_parse = ET.fromstring(msg['body'])
                start_time = float(msg_parse.attrib['time'])
                delta_time = (end_time - start_time) / 2
                self.update_topo_package('B', delta_time)
            elif msg['body'][1:5] == "pack":
                parse = ET.fromstring(msg['body'])
                pack_json = parse.attrib['lsa']
                lsa = json.loads(pack_json)
                print("Recieved a pack", lsa)

            else:
                pass
