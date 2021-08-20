#libraries
from _typeshed import NoneType
import asyncio
import logging
from aioconsole import aprint

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import xml.etree.ElementTree as ET


class Node(slixmpp.ClientXMPP):

    """
    Class for manage client conection and functionalities
    -------------------------------------------------------------------
    PARAMETERS: 
    jid : str
        JID of user
    password : str
        user password
    is_new : boolean, optional
        indicates if user is registering or authenticating
    """
    def __init__(self, jid, password, nickname=None, is_new=False):
        super().__init__(jid, password)

        if not nickname:
            self.nick = jid.split('@')[0]
        else:
            self.nick = nickname
    
        # Event for maganage conection
        self.connected_event = asyncio.Event()

        #handlers for manage triggers
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.add_event_handler('register', self.register)

        #necessary plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # Ping

        if is_new:
            self.register_plugin('xep_0077') # In-band Registration        
            self.register_plugin('xep_0004') # Data forms
            self.register_plugin('xep_0066') # Out-of-band Data
            self['xep_0077'].force_registration = True


    """
    Corrutine for register a new user 
    """        
    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

    """
    Corrutine for manage start session
    """
    async def start(self, event):
        try:
            self.send_presence() #<presence />
            await self.get_roster() #IQ stanza for retrieve, response is saved by internal handler (self.roster)
            self.connected_event.set()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')

    """
    Corrutine for recieve messages
    """
    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            await aprint("\n{}".format(msg['body']))

    """
    Function for send messages
    """
    def message_to(self, mto, body):
        self.send_message(
            mfrom=self.boundjid,
            mto=mto,
            mbody=body, #body should go with Network layer attributes
            mnick=self.nick
        )
   