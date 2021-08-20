# Laboratorio 3 Redes - 2021
Client that implements XMPP protocol to test routing algorithms.
Domain `alumchat.xyz`


## Requirements
* Python 3.8.*
slixmpp ([docs](https://slixmpp.readthedocs.io/en/latest/))


## How to Use
1. Download client.py
2. Make sure *python* version is correct.
3. Make sure all *requirements* and *libraries* are installed.
4. Run (multiple ways)
```
python3 client.py
```
```
python3 client.py -j [your JID] -p [your password]
```
```
python3 client.py -j [your JID]
```

## Components
File | Description |
:---: | :---: |
main | Contains main XMPP client to test algorithms. |
module | Contains util functions. |
RoutingTable | Contains routing table class and triplet struct. |


## Autor
- *Luis Quezada* - [@Lfquezada](https://github.com/Lfquezada)
- *Roberto Figueroa* - [@RobertoFigueroa](https://github.com/RobertoFigueroa)
- *Esteban del Valle* - [@Estdv](https://github.com/Estdv)

## Fuentes
* https://www.geeksforgeeks.org/distance-vector-routing-dvr-protocol/