#Awaiting message format
#Awaiting xmpp message infrastructure

def flooding(topo, names,msg,jid):

    #Se extrae el nodo que somos
    jids = list(names.values())
    noms = list(names.keys())
    position = jids.index(jid)
    nombre = noms[position]
    
    #Se escucha por menajes
    #if llega mensaje:
    
        #Se verifica en el mensaje que no seamos el nodo destino
    
        if (msg[destino] != nombre):
            #Se obtiene el nombre de todos los nodos hijos
            hijos = topo[config[nombre]]

            #Se envia el mensaje a todos los nodos hijos
            for i in hijos:
                #send msg[mensaje] to i
