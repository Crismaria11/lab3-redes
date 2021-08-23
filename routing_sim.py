import asyncio
import logging
import getpass
from aioconsole.stream import aprint
from optparse import OptionParser

from node import Node
from aioconsole import ainput

from module import *
from RoutingTable import *

from LSR import LSR

"""
Function that manages UI
"""
async def main(node : LSR):
    
    """
    Aqui agregar la implementacion de cada algoritmo
    """

    for router in node.neighbors_niknames:
        node.send_presence_subscription(node.neighbors[router], node.boundjid)


    node.init_listener()


    is_connected = True
    while is_connected:
        print("-"*20) 
        print("Choose an algorithm:\n1.Flooding\n2.DVR\n3.LSR")
        opt = int( await ainput("Choose an option\n->"))
        if opt == 1:
            #initilize flooding algorithm
            pass 
        elif opt == 2:
            #initialize dvr algorithm
            pass
        elif opt == 3:
            #initialize lsr algorithm
            pass
        else:
            #default algorithm or exit
            pass

        


if __name__ == "__main__":

    optp = OptionParser()

    optp.add_option('-d', '--debug', help='set loggin to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-n", "--new", dest="is_new",
                    help="is registering a new user", 
                    action='store_const',
                    const=True, default=False)

    optp.add_option("-r", "--router", dest="router",
                    help="router nickname")

    opts, args = optp.parse_args()

    if opts.jid is None:
        opts.jid = input("Username (JID): ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")  
    if opts.router is None:
        opts.router = input("Router nickname")

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')


    assignedNode = opts.router
    topo = infoGetter(assignedNode,'topo.txt')
    names = infoGetter(assignedNode,'names.txt')
    assignedNodes = {}
    for i in topo:
        assignedNodes[i] = names[i]    

    try:
        node = LSR(opts.jid, opts.password, assignedNode, assignedNodes)
        if opts.is_new:
            print("Registrando ...")
        print("Conectando ....")
        node.connect() 
        node.loop.run_until_complete(node.connected_event.wait())
        node.loop.create_task(main(node))
        node.process(forever=False)
    except Exception as e:
        print("Error:", e)
    finally:
        node.disconnect()
