from slixmpp.basexmpp import BaseXMPP
from node import Node

from asyncio import sleep
from aioconsole import aprint


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

    def send_hello(self, hto, hfrom):
        """
        Function for neighbor discovery
        """
        self.send_message(hto, "Hello")

    def eco(self):
        """
        Function for measure cost between neighbors
        """
        return {}

    def build_topo_package(self):
        """
        Function for package build about the network
        """
        
        return {}

    def send_topo_package(self):
        """
        Send the topo package to neighbors
        """
        return "This must be a message stanza with self.LSA"
    
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
