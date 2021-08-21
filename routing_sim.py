import logging
import getpass
from aioconsole.stream import aprint
from optparse import OptionParser

from node import Node
from aioconsole import ainput

"""
Function that manages UI
"""
async def main(node : Node):
    global msg
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


    opts, args = optp.parse_args()

    if opts.jid is None:
        opts.jid = input("Username (JID): ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")  

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    try:
        node = Node(opts.jid, opts.password, opts.is_new)
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
