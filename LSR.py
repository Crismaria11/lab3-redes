# from slixmpp.basexmpp import BaseXMPP


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

class LSR(object):
    
    def __init__(self):
        self.LSA_seqnum = 0
        self.LSA = {}
    
    def send_hello(self):
        """
        Function for neighbor discovery
        """
        return []

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
