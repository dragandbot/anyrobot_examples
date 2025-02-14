#!/usr/bin/python3

# Assumed a Simbot is running (drag&bot Robot Simulator)

# This example shows how to get and set digital IOs
# Digital Output will be read, then set the inverted value and then read again
# Use Ctrl+C to stop the program

import websocket # websocket-client https://github.com/websocket-client/websocket-client
import json      # default supported by python
import uuid      # for generating unique ids in a easy way, part of the inbuilt python packages
import ssl

MAC_AUTH = # SET MAC STRING HERE (see: https://wiki.ros.org/rosauth)

if __name__ == "__main__":
    connection_ip = "192.168.100.100" # Loopback localhost address, assuming running in same computer
    connection_port = 80              # If SSL is activated on the controller use port 443
    connection_protocol = "ws://"     # If SSL is activated use protocol 'wss://'

    connection_uri = connection_protocol + connection_ip + ":" + str(connection_port) + '/dnb-rosbridge'

    ### NO SSL ###
    ws = websocket.create_connection(connection_uri, timeout=10)

    ### SSL activated ########
    # Uncomment the following code if you are using a self signed certificate on the controller
    # **NOT RECOMMENDED FOR PRODUCTION USAGE.** sslopt dict disables certificate verification.
    #ssl_options = {"cert_reqs": ssl.CERT_NONE}

    # Synchronous connection for this example
    #ws = websocket.create_connection(connection_uri, sslopt=ssl_options, timeout=10)
    ### End: SSL activated ###

    # Auth service call needs to be set directly on the first request after established connection
    auth_service = {
        "op": "auth",
        "client": "my-client",
        "dest": "ros",
        "end": 0,
        "level": "admin",
        "mac": MAC_AUTH,
        "rand": "rand",
        "t": 0
    }
    ws.send(json.dumps(auth_service))

    # Get one digital IO
    # / at the beginning of a service id is optional
    # As example in this case we ignore id
    get_request = {
        "op": "call_service",
        "service": "/robot/get_digital_ios",
        "args": { "ios":
                    [
                        {
                            "group_id": "DO",
                            "pin_number": 1
                        }
                    ]
                }
        }

    ws.send(json.dumps(get_request))
    response = json.loads(ws.recv())
    # In this case, response comes without id field

    io_value = bool(response["values"]["ios"][0]["value"]) # Parse field as boolean
    print("Digital Output original value: " + str(io_value))

    new_io_value = not io_value # Invert the value

    # In this request, as example, we write one id to show how it works
    set_request_id = str(uuid.uuid4())

    set_request = {
        "op": "call_service",
        "service": "/robot/set_digital_ios",
        "args": { "ios":
                    [
                        {   "id":
                                {
                                    "group_id": "DO",
                                    "pin_number": 1
                                },
                            "value": new_io_value
                        }
                    ]
                },
        "id": set_request_id
        }

    # Write digital output
    ws.send(json.dumps(set_request))
    set_response = json.loads(ws.recv())

    assert(set_response["id"] == set_request_id) # Check we receive the same id

    # Read digital output again
    ws.send(json.dumps(get_request))
    response = json.loads(ws.recv())

    io_value = bool(response["values"]["ios"][0]["value"]) # Parse field as boolean
    print("Digital Output current value: " + str(io_value))

    ws.close()



