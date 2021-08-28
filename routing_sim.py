import asyncio
import logging
import getpass
from aioconsole.stream import aprint
from optparse import OptionParser

from node import Node
from aioconsole import ainput

from module import *


from LSR import LSR
from FLOOD import Flood
from DVR import DVR

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
        print("Choose an option:\n1.Send message\n2.Exit")
        opt = int( await ainput("Choose an option\n->"))
        if opt == 1:
            dest = await ainput("Write jid dest: ")
            msg = await ainput("Write message: ")
            node.send_msg(
                dest,
                msg
            )
        elif opt == 2:
            node.is_offline = True
            print("Disconnecting ...")
            await asyncio.sleep(10)
            is_connected = False
            node.disconnect()
        else:
            pass

        


if __name__ == "__main__":

    optp = OptionParser()

    t_k = keys("topo.txt")

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
    optp.add_option("-a", "--algorithm", dest="algorithm",
                    help="algorithm to use")

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

    if opts.algorithm == 'flooding':
        node = Flood(opts.jid, opts.password, assignedNode, assignedNodes)
    elif opts.algorithm == 'dvr':
        node = DVR(opts.jid, opts.password, assignedNode, assignedNodes, t_keys=t_k)
    elif opts.algorithm == 'lsr':
        node = LSR(opts.jid, opts.password, assignedNode, assignedNodes)
    else:
        node = None

    if node != None:
        try:
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
    else:
        print("Algorithm not selected, run again with -a")
