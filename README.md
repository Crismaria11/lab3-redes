# Laboratorio 3 Redes - 2021
Client that implements XMPP protocol to test routing algorithms.<br>
Domain `alumchat.xyz`


## Requirements
* Python 3.8.*
* slixmpp 1.7.1 ([docs](https://slixmpp.readthedocs.io/en/latest/))
* aioconsole 0.3.2
* aiodns==3.0.0
* asyncio==3.4.3
* cffi==1.14.6
* numpy==1.21.2
* pyasn1==0.4.8
* pyasn1-modules==0.2.8
* pycares==4.0.0
* pycparser==2.20
* scipy==1.7.1

## How to Use
1. Download all python files.
2. Make sure *python* version is correct.
3. Make sure all *requirements* and *libraries* are installed.
```
pip3 install -r requirements.txt
```
4. Run (multiple ways)
```
python3 routing_sim.py -j [your JID] -p [your password] -a [flooding/dvr/lsr]
```

## Testing Topology & Test Users
* A: _a@alumchat.xyz | Connected to: B,C
* B: _b@alumchat.xyz | Connected to: A
* C: _c@alumchat.xyz | Connected to: A,D
* D: _d@alumchat.xyz | Connected to: C

## Tags
Tag | Description |
:---: | :---: |
msg | Indicates that a message is being sent. |
eco | Indicates that response time is being calculated for node distance metrics. |
a_eco | *ackknowledge* eco is a postive response from a node's response time calculation. |
hello | Indicates the presence of a node in the network. |
pack | Indicates the presence of a node in the network. |
flood | Allows to identify a message as flooding for it's correct sending/dropping. |

## Algorithms Implemented
Algorithm | Description |
:---: | :---: |
Flooding | Does not require topology or cost information. Each received packet is forwarded to neighboring nodes except for the one that sent it. The advantage of this algorithm is that the shortest path will always be found if it exists by means of a hop counter since all possible options are tried. |
DVR | Also called Bellman-Ford algorithm, consists of a router informing its neighbors periodically of changes in the topology. Each router has an information vector that stores the distance to each existing node. A router broadcasts its distance to all its neighbors in a routing packet. Each router receives and saves the vector most recently. Finally, it recalculates its distance vector when it receives a vector with different information than before. |
LSR | Link state routing uses link state routers to exchange messages to learn the entire network topology. Each router calculates its routing table using the shortest path algorithm (Dijkstra). All nodes in the topology must be trusted. |

## Authors
- *Roberto Figueroa* - [@RobertoFigueroa](https://github.com/RobertoFigueroa)
- *Luis Quezada* - [@Lfquezada](https://github.com/Lfquezada)
- *Esteban del Valle* - [@Estdv](https://github.com/Estdv)

## References
* Franchitti, J. (s.f.). Routing algorithms and routing protocols. New York University. Department of Computer science.  
* GeeksForGeeks. (2019). Distance Vector Routing (DVR) Protocol. From https://www.geeksforgeeks.org/distance-vector-routing-dvr-protocol/
* GeeksForGeeks. (2019).Fixed and Flooding Routing algorithms. From https://www.geeksforgeeks.org/fixed-and-flooding-routing-algorithms/
* GeeksForGeeks. (2021). Unicast Routing – Link State Routing. From https://www.geeksforgeeks.org/unicast-routing-link-state-routing/
* Tenenbaum, A y Wetheral, D. (2012). Redes de computadoras. Quinta edición. Editorial Pearson. México.
